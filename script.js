script_js_v2 = """const tracks = [
  {
    title: "Demo Track from Telegram",
    file_id: "BQACAgQAAxkBAAI123Zl...demo_file_id...",
    type: "telegram"
  },
  {
    title: "External MP3 File",
    url: "https://example.com/audio.mp3",
    type: "external"
  }
];

function search() {
  const query = document.getElementById("query").value.toLowerCase();
  const results = tracks.filter(t => t.title.toLowerCase().includes(query));
  render(results);
}

function render(list) {
  const container = document.getElementById("playlist");
  container.innerHTML = "";

  list.forEach(track => {
    const div = document.createElement("div");
    div.className = "track";
    div.innerHTML = `
      <div>${track.title}</div>
      <button onclick='play("${track.type}", "${track.file_id || track.url}")'>▶️</button>
    `;
    container.appendChild(div);
  });
}

function play(type, ref) {
  if (type === "external") {
    const audio = new Audio(ref);
    audio.play();
  } else if (type === "telegram") {
    const token = "YOUR_TELEGRAM_BOT_TOKEN";
    fetch(`https://api.telegram.org/bot${token}/getFile?file_id=${ref}`)
      .then(res => res.json())
      .then(data => {
        const path = data.result.file_path;
        const audioUrl = `https://api.telegram.org/file/bot${token}/${path}`;
        const audio = new Audio(audioUrl);
        audio.play();
      });
  }
}"""
