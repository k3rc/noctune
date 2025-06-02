const tg = window.Telegram.WebApp;
tg.expand();

let playlist = [];

function renderPlaylist() {
  const list = document.getElementById("playlist");
  list.innerHTML = "";

  playlist.forEach((track, index) => {
    const div = document.createElement("div");
    div.className = "track";
    div.innerHTML = `
      <div class="track-title">${track}</div>
      <button onclick="playTrack(${index})">▶️</button>
    `;
    list.appendChild(div);
  });
}

function addTrack() {
  const input = document.getElementById("query");
  const value = input.value.trim();
  if (!value) return;
  playlist.push(value);
  renderPlaylist();
  input.value = "";
  // Здесь можно отправить запрос на сервер или в Telegram initData
}

function playTrack(index) {
  alert("Воспроизведение: " + playlist[index]);
}