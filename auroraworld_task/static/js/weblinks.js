document.addEventListener("DOMContentLoaded", function () {
    fetchWebLinks();
});

function fetchWebLinks() {
    fetch("/feedmanager/all_links/")
        .then(response => response.json())
        .then(data => {
            let webLinkList = document.getElementById("webLinkList");
            webLinkList.innerHTML = ""; // 기존 목록 초기화

            if (data.weblinks.length === 0) {
                webLinkList.innerHTML = "<p>등록된 웹 링크가 없습니다.</p>";
                return;
            }

            data.weblinks.forEach(link => {
                let li = document.createElement("li");
                li.innerHTML = `
                    <strong>${link.name}</strong> - 
                    <a href="${link.url}" target="_blank">${link.url}</a> 
                    (${link.category})
                    <button onclick="openEditModal(${link.id}, '${link.name}', '${link.url}')">수정</button>
                `;
                webLinkList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching web links:", error));
}

/* ✅ 웹 링크 수정 기능 (등록 관련 함수 삭제됨) */
function openEditModal(id, name, url) {
    document.getElementById("editWebLinkId").value = id;
    document.getElementById("editWebLinkName").value = name;
    document.getElementById("editWebLinkUrl").value = url;
    document.getElementById("editModal").style.display = "block";
}

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

function updateWebLink() {
    let id = document.getElementById("editWebLinkId").value;
    let name = document.getElementById("editWebLinkName").value.trim();
    let url = document.getElementById("editWebLinkUrl").value.trim();

    if (!name || !url) {
        alert("수정할 웹 링크 이름과 URL을 입력하세요!");
        return;
    }

    fetch(`/feedmanager/edit/${id}/`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ name, url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("수정 실패: " + data.error);
        } else {
            alert("웹 링크가 수정되었습니다!");
            closeEditModal();
            fetchWebLinks(); // 새로고침 없이 목록 업데이트
        }
    })
    .catch(error => console.error("Error:", error));
}

function getCSRFToken() {
    let cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") return value;
    }
    return "";
}

// ESC 키로 모달 닫기
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeEditModal();
    }
});

function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

function deleteWebLink() {
    let id = document.getElementById("editWebLinkId").value;

    if (!id) {
        alert("삭제할 웹 링크를 선택하세요!");
        return;
    }

    if (!confirm("정말 삭제하시겠습니까?")) {
        return;  // 사용자가 취소하면 실행하지 않음
    }

    fetch(`/feedmanager/delete/${id}/`, {
        method: "DELETE",
        headers: {
            "X-CSRFToken": getCSRFToken()
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || "삭제 실패"); });
        }
        return response.json();
    })
    .then(data => {
        alert("웹 링크가 삭제되었습니다!");
        closeEditModal();
        fetchWebLinks();  // 목록 새로고침
    })
    .catch(error => {
        console.error("Error:", error);
        alert("삭제 중 오류 발생: " + error.message);
    });
}

window.deleteWebLink = deleteWebLink;