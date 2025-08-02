// Cloudflare Worker for Telegram File Proxy
// Updated for 4GB files and better forwarded file handling

addEventListener("fetch", (event) => {
  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Handle CORS
  if (request.method === "OPTIONS") {
    return new Response(null, {
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "Range, Accept-Ranges",
        "Access-Control-Max-Age": "86400",
      },
    });
  }

  // Handle streaming requests
  if (path.startsWith("/stream/") || path.startsWith("/dl/")) {
    return handleStreamRequest(request, path);
  }

  // Handle API requests
  if (path.startsWith("/api/")) {
    return handleApiRequest(request, path);
  }

  // Default response
  return new Response("Telegram File Proxy Worker - Supports up to 4GB files", {
    headers: { "Content-Type": "text/plain" },
  });
}

async function handleStreamRequest(request, path) {
  try {
    // Extract file info from path
    const parts = path.split("/");
    const action = parts[1]; // 'stream' or 'dl'
    const fileId = parts[2];
    const hash = parts[3] || "";

    console.log(`Processing ${action} request for fileId: ${fileId}`);

    // Get file info from Telegram
    const fileInfo = await getTelegramFileInfo(fileId);
    console.log(`File info response:`, fileInfo);

    if (!fileInfo.ok) {
      console.log(`File info failed, trying forwarded file approach`);
      // Try alternative approach for forwarded files
      return handleForwardedFile(request, fileId);
    }

    const filePath = fileInfo.result.file_path;
    const fileSize = fileInfo.result.file_size;

    // Check file size (4GB limit)
    const maxSize = 4 * 1024 * 1024 * 1024; // 4GB
    if (fileSize > maxSize) {
      return new Response(`File too large. Maximum size is 4GB`, {
        status: 413,
      });
    }

    // Create direct Telegram file URL
    const telegramUrl = `https://api.telegram.org/file/bot${TELEGRAM_BOT_TOKEN}/${filePath}`;

    // Proxy the file with range support
    const response = await fetch(telegramUrl, {
      headers: {
        Range: request.headers.get("Range") || "",
        "User-Agent": "TelegramBot/1.0",
      },
    });

    if (!response.ok) {
      return new Response("Failed to fetch file", { status: 500 });
    }

    // Return proxied response
    return new Response(response.body, {
      status: response.status,
      headers: {
        "Content-Type": "video/mp4",
        "Content-Length": fileSize.toString(),
        "Accept-Ranges": "bytes",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD",
        "Access-Control-Allow-Headers": "Range",
        "Cache-Control": "public, max-age=3600",
        "Content-Disposition": `inline; filename="video.mp4"`,
      },
    });
  } catch (error) {
    return new Response(`Error: ${error.message}`, { status: 500 });
  }
}

async function handleForwardedFile(request, fileId) {
  try {
    console.log(`Trying forwarded file approach for fileId: ${fileId}`);

    // For forwarded files, try direct access
    const directUrl = `https://api.telegram.org/file/bot${TELEGRAM_BOT_TOKEN}/${fileId}`;
    console.log(`Direct URL: ${directUrl}`);

    const response = await fetch(directUrl, {
      headers: {
        Range: request.headers.get("Range") || "",
        "User-Agent": "TelegramBot/1.0",
      },
    });

    console.log(`Direct URL response status: ${response.status}`);

    if (!response.ok) {
      console.log(`Direct URL failed with status: ${response.status}`);
      return new Response(
        `Forwarded file not accessible (Status: ${response.status})`,
        {
          status: 403,
          headers: {
            "Content-Type": "text/plain",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
    }

    // Return direct response for forwarded files
    return new Response(response.body, {
      status: response.status,
      headers: {
        "Content-Type": "video/mp4",
        "Accept-Ranges": "bytes",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD",
        "Access-Control-Allow-Headers": "Range",
        "Cache-Control": "public, max-age=3600",
        "Content-Disposition": `inline; filename="forwarded_video.mp4"`,
      },
    });
  } catch (error) {
    console.log(`Forwarded file error: ${error.message}`);
    return new Response(`Forwarded file error: ${error.message}`, {
      status: 500,
      headers: {
        "Content-Type": "text/plain",
        "Access-Control-Allow-Origin": "*",
      },
    });
  }
}

async function handleApiRequest(request, path) {
  try {
    const url = new URL(request.url);
    const fileId = url.searchParams.get("file_id");

    if (!fileId) {
      return new Response("Missing file_id parameter", { status: 400 });
    }

    // Get file info
    const fileInfo = await getTelegramFileInfo(fileId);

    if (!fileInfo.ok) {
      // Try alternative for forwarded files
      const streamUrl = `${url.origin}/stream/${fileId}`;
      const downloadUrl = `${url.origin}/dl/${fileId}`;

      return new Response(
        JSON.stringify({
          success: true,
          file_size: "Unknown (forwarded file)",
          stream_url: streamUrl,
          download_url: downloadUrl,
          note: "Forwarded file - direct access",
        }),
        {
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
        }
      );
    }

    const filePath = fileInfo.result.file_path;
    const fileSize = fileInfo.result.file_size;

    // Create streaming URLs
    const streamUrl = `${url.origin}/stream/${fileId}`;
    const downloadUrl = `${url.origin}/dl/${fileId}`;

    return new Response(
      JSON.stringify({
        success: true,
        file_size: fileSize,
        stream_url: streamUrl,
        download_url: downloadUrl,
      }),
      {
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
      }),
      {
        status: 500,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
        },
      }
    );
  }
}

async function getTelegramFileInfo(fileId) {
  const response = await fetch(
    `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getFile`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ file_id: fileId }),
    }
  );

  return await response.json();
}

// Get bot token from environment variables
const TELEGRAM_BOT_TOKEN = "8445456449:AAGE0BaW2pSxJf7t4j5wb0Q09KRPItienPA";
