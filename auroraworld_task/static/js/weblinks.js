document.addEventListener("DOMContentLoaded", function () {
    fetchWebLinks();
});

// ✅ 웹 링크 목록 가져오기 및 "공유하기" 버튼 추가
function fetchWebLinks() {
    fetch("/feedmanager/all_links/")
        .then(response => response.json())
        .then(data => {
            let webLinkList = document.getElementById("webLinkList");
            webLinkList.innerHTML = ""; 

            if (data.weblinks.length === 0) {
                webLinkList.innerHTML = "<p>등록된 웹 링크가 없습니다.</p>";
                return;
            }

            data.weblinks.forEach(link => {
                let li = document.createElement("li");
                li.classList.add("web-link-item");

                li.innerHTML = `
                    <div class="web-link-info">
                        <strong>${link.name}</strong> - 
                        <a href="${link.url}" target="_blank">${link.url}</a> 
                        (${link.category})
                    </div>
                    <div class="web-link-buttons">
                        <button class="share-btn" onclick="openShareModal(${link.id})">공유하기</button>
                        <button class="edit-btn" onclick="openEditModal(${link.id}, '${link.name}', '${link.url}')">수정</button>
                        <button class="delete-btn" onclick="deleteWebLink(${link.id})">삭제</button>
                    </div>
                    <div class="share-box" id="shareBox-${link.id}" style="display:none;">
                        <input type="text" id="searchUserInput-${link.id}" placeholder="이름, 이메일, ID 검색" onkeyup="searchUsers(${link.id})">
                        <ul id="userList-${link.id}"></ul>
                        <button class="close-btn" onclick="closeShareBox(${link.id})">닫기</button>
                    </div>
                `;
                webLinkList.appendChild(li);
            });
        })
        .catch(error => console.error("Error fetching web links:", error));
}

// // ✅ 공유 박스 열기 / 닫기 토글
// function toggleShareBox(webLinkId) {
//     let shareBox = document.getElementById(`shareBox-${webLinkId}`);
//     if (shareBox.style.display === "none") {
//         shareBox.style.display = "block";
//         fetchUsers(webLinkId);
//     } else {
//         shareBox.style.display = "none";
//     }
// }

// // ✅ 공유 박스 닫기
// function closeShareBox(webLinkId) {
//     document.getElementById(`shareBox-${webLinkId}`).style.display = "none";
// }

// ✅ 사용자 목록 불러오기
function fetchUsers(webLinkId) {
    fetch("/users/all_users/")
        .then(response => response.json())
        .then(data => {
            console.log("✅ 사용자 목록 응답:", data); // JSON 응답 확인

            let userList = document.getElementById("userList");
            userList.innerHTML = ""; // ✅ 기존 목록 초기화
            userList.style.display = "none"; // ✅ 기본적으로 숨김

            data.users.forEach(user => {
                let username = user.username || "알 수 없음";
                let name = user.name || "알 수 없음";
                let email = user.email || "알 수 없음";

                let li = document.createElement("li");
                li.dataset.username = username;  // ✅ 검색을 위한 데이터 속성 추가
                li.dataset.name = name;
                li.dataset.email = email;
                li.textContent = `${username} (${name}, ${email})`; // ✅ ID 제외하고 표시

                li.onclick = function () {
                    shareWebLink(webLinkId, user.id);
                };
                userList.appendChild(li);
            });

            // ✅ 여기서 userList.style.display = "block"; 를 실행하지 않음

        })
        .catch(error => console.error("❌ 사용자 목록 불러오기 실패:", error));
}




function openShareModal(webLinkId) {
    let shareModal = document.getElementById("shareModal");
    shareModal.style.display = "block"; // ✅ 모달 표시
    document.getElementById("searchUserInput").dataset.webLinkId = webLinkId; // ✅ 공유할 웹 링크 ID 저장
    fetchUsers(webLinkId); // ✅ 사용자 목록 불러오기
}
// ✅ 공유 모달 닫기
function closeShareModal() {
    document.getElementById("shareModal").style.display = "none"; 
}
// ✅ ESC 키로 공유 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeShareModal();
    }
});


// ✅ 사용자 검색 기능 (이메일 또는 이름으로 검색 가능)
function searchUsers() {
    let input = document.getElementById("searchUserInput").value.toLowerCase();
    let userList = document.getElementById("userList"); // ✅ 사용자 목록
    let users = document.querySelectorAll("#userList li");

    let hasResults = false; // ✅ 검색 결과가 있는지 확인

    users.forEach(user => {
        let userText = user.dataset.username.toLowerCase(); // ✅ username으로 기본 검색
        let userNameText = user.dataset.name.toLowerCase();
        let userEmailText = user.dataset.email.toLowerCase();

        if (
            userText.includes(input) ||  // ✅ 기본 username 검색
            userNameText.includes(input) || // ✅ 이름(name) 검색
            userEmailText.includes(input)  // ✅ 이메일(email) 검색
        ) {
            user.style.display = "block";
            hasResults = true; // ✅ 검색 결과 있음
        } else {
            user.style.display = "none";
        }
    });

    if (input.length > 0 && hasResults) {
        userList.style.display = "block"; // ✅ 검색 결과 있으면 목록 표시
    } else {
        userList.style.display = "none"; // ✅ 검색 결과 없으면 숨김
    }
}






// ✅ 웹 링크 공유 기능
function shareWebLink(userId) {
    let webLinkId = document.getElementById("searchUserInput").dataset.webLinkId;

    fetch("/feedmanager/share/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ webLinkId, userId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("공유 실패: " + data.error);
        } else {
            alert("웹 링크가 공유되었습니다!");
            closeShareModal();
        }
    })
    .catch(error => console.error("Error sharing web link:", error));
}


// ✅ 웹 링크 수정 기능
function openEditModal(id, name, url) {
    document.getElementById("editWebLinkId").value = id;
    document.getElementById("editWebLinkName").value = name;
    document.getElementById("editWebLinkUrl").value = url;
    document.getElementById("editModal").style.display = "block";
}

// ✅ Enter 키로 수정 버튼 작동
document.getElementById("editModal").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        updateWebLink();
    }
});

// ✅ 수정 모달 닫기
function closeEditModal() {
    document.getElementById("editModal").style.display = "none";
}

// ✅ 웹 링크 업데이트
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

// ✅ 웹 링크 삭제
function deleteWebLink(id) {
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
        fetchWebLinks();  // 목록 새로고침
    })
    .catch(error => {
        console.error("Error:", error);
        alert("삭제 중 오류 발생: " + error.message);
    });
}

// ✅ CSRF 토큰 가져오기
function getCSRFToken() {
    let cookies = document.cookie.split("; ");
    for (let cookie of cookies) {
        let [name, value] = cookie.split("=");
        if (name === "csrftoken") return value;
    }
    return "";
}

// ✅ ESC 키로 수정 모달 닫기
document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        closeEditModal();
    }
});

// ✅ 공유받은 웹 링크 목록 가져오기
function fetchSharedWebLinks() {
    console.log("📢 fetchSharedWebLinks() 실행됨! ✅");

    fetch("/feedmanager/shared_links/")
        .then(response => {
            console.log("📢 API 요청 응답 상태 코드:", response.status); // 응답 코드 확인
            return response.json();
        })
        .then(data => {
            console.log("📢 API 응답 데이터:", data); // 응답 데이터 확인

            let sharedWebLinkList = document.getElementById("sharedWebLinkList");

            if (!sharedWebLinkList) {
                console.error("❌ 오류: 공유받은 링크를 표시할 #sharedWebLinkList 요소를 찾을 수 없음!");
                return;
            }

            sharedWebLinkList.innerHTML = "";

            if (data.shared_links.length === 0) {
                sharedWebLinkList.innerHTML = "<p>공유받은 웹 링크가 없습니다.</p>";
                return;
            }

            data.shared_links.forEach(link => {
                let li = document.createElement("li");
                li.innerHTML = `<strong>${link.name}</strong> - 
                                <a href="${link.url}" target="_blank">${link.url}</a> 
                                (${link.category}) | 공유한 사용자: ${link.shared_by}`;
                sharedWebLinkList.appendChild(li);
            });
        })
        .catch(error => console.error("❌ 공유 웹 링크 불러오기 실패:", error));
}


// ✅ 로그인 후 공유받은 웹 링크 자동 로드
document.addEventListener("DOMContentLoaded", function () {
    fetchSharedWebLinks();
});

// ✅ 웹 링크 공유 기능 (디버깅 추가)
function shareWebLink(userId) {
    let webLinkId = document.getElementById("searchUserInput").dataset.webLinkId;

    console.log(`📢 공유 요청: 웹 링크 ID: ${webLinkId}, 공유 대상 ID: ${userId}`);

    fetch("/feedmanager/share/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ webLinkId, userId })
    })
    .then(response => response.json())
    .then(data => {
        console.log("📢 서버 응답:", data);
        if (data.error) {
            alert("공유 실패: " + data.error);
        } else {
            alert("웹 링크가 공유되었습니다!");
            closeShareModal();
            fetchSharedWebLinks(); // ✅ 공유받은 웹 링크 목록 업데이트
        }
    })
    .catch(error => console.error("❌ 공유 중 오류 발생:", error));
}



// ✅ window 객체에 삭제 함수 등록 (HTML에서 사용 가능하도록)
window.deleteWebLink = deleteWebLink;
