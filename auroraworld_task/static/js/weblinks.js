document.addEventListener("DOMContentLoaded", function () {
    fetchWebLinks();
});

function fetchWebLinks() {
    fetch("/feedmanager/all_links/")
        .then(response => response.json())
        .then(data => {
            let webLinkList = document.getElementById("webLinkList");
            webLinkList.innerHTML = "";  // 기존 목록 초기화

            if (data.weblinks.length === 0) {
                webLinkList.innerHTML = "<p>등록된 웹 링크가 없습니다.</p>";
                return;
            }

            data.weblinks.forEach(link => {
                let li = document.createElement("li");
                li.innerHTML = `<strong>${link.name}</strong> - <a href="${link.url}" target="_blank">${link.url}</a> (${link.category})`;
                webLinkList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching web links:", error));
}
