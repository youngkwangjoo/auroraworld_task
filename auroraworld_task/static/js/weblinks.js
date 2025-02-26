document.addEventListener("DOMContentLoaded", function () {
    fetchWebLinks();
});

// ✅ 웹 링크 목록 가져오기 
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

// ✅ 사용자 목록 불러오기
// function fetchUsers(webLinkId) {
//     fetch("/users/all_users/")
//         .then(response => response.json())
//         .then(data => {
//             console.log("✅ 사용자 목록 응답:", data);

//             let userList = document.getElementById("userList");
//             userList.innerHTML = "";
//             userList.style.display = "none";

//             // ✅ 전체 사용자에게 공유 버튼 추가
//             let shareAllBtn = document.createElement("button");
//             shareAllBtn.textContent = "📢 전체 공유";
//             shareAllBtn.classList.add("share-all-btn");
//             shareAllBtn.onclick = function () {
//                 console.log(`📢 [DEBUG] 전체 공유 실행 - 웹 링크 ID: ${webLinkId}`);

//                 let allUserIds = data.users.map(user => parseInt(user.id));  // 모든 userId 배열화
//                 shareWebLinkMultiple(webLinkId, allUserIds);
//             };
//             userList.appendChild(shareAllBtn);

//             data.users.forEach(user => {
//                 let li = document.createElement("li");
//                 li.dataset.userId = user.id;
//                 li.dataset.username = user.username || "";
//                 li.dataset.name = user.name || "";
//                 li.dataset.email = user.email || "";

//                 li.textContent = `${user.username} (${user.name}, ${user.email})`;

//                 // ✅ 클릭한 사용자에게 개별 공유 실행
//                 li.onclick = function () {
//                     console.log(`📢 [DEBUG] 클릭된 사용자 - userId: ${li.dataset.userId}, username: ${li.dataset.username}`);

//                     // ✅ 개별 공유 실행
//                     shareWebLink(webLinkId, parseInt(li.dataset.userId));
//                 };

//                 userList.appendChild(li);
//             });

//             console.log("📢 업데이트된 사용자 목록:", userList.innerHTML);
//         })
//         .catch(error => console.error("❌ 사용자 목록 불러오기 실패:", error));
// }






// ✅ 클릭된 사용자 음영처리 효과
function highlightSelection(element) {
    element.style.backgroundColor = "#d3d3d3"; // 클릭 시 회색 음영 처리
    setTimeout(() => {
        element.style.backgroundColor = ""; // 0.3초 후 원래 색상으로 복귀
    }, 300);
}


// function openShareModal(webLinkId) {
//     let shareModal = document.getElementById("shareModal");
//     shareModal.style.display = "block"; // ✅ 모달 표시
//     document.getElementById("searchUserInput").dataset.webLinkId = webLinkId; // ✅ 공유할 웹 링크 ID 저장
//     fetchUsers(webLinkId); // ✅ 사용자 목록 불러오기
// }
// // ✅ 공유 모달 닫기
// function closeShareModal() {
//     document.getElementById("shareModal").style.display = "none"; 
// }
// // ✅ ESC 키로 공유 모달 닫기
// document.addEventListener("keydown", function (event) {
//     if (event.key === "Escape") {
//         closeShareModal();
//     }
// });

// ✅ 사용자 검색 기능 (이메일 또는 이름으로 검색 가능)
// function searchUsers() {
//     let input = document.getElementById("searchUserInput").value.toLowerCase();
//     let userList = document.getElementById("userList");
//     let users = document.querySelectorAll("#userList li");

//     let hasResults = false;

//     users.forEach(user => {
//         let userText = (user.dataset.username || "").toLowerCase();
//         let userNameText = (user.dataset.name || "").toLowerCase();
//         let userEmailText = (user.dataset.email || "").toLowerCase();

//         if (
//             userText.includes(input) ||
//             userNameText.includes(input) ||
//             userEmailText.includes(input)
//         ) {
//             user.style.display = "block";
//             hasResults = true;

//             // ✅ 기존 이벤트 제거 후 다시 추가
//             user.onclick = null;
//             user.onclick = function () {
//                 let selectedUserId = parseInt(user.dataset.userId);
//                 console.log(`📢 [DEBUG] 검색 후 선택된 사용자 - userId: ${selectedUserId}, username: ${user.dataset.username}`);

//                 // ✅ 선택된 userId를 searchUserInput에 저장
//                 document.getElementById("searchUserInput").dataset.selectedUserId = selectedUserId;

//                 shareWebLink(parseInt(document.getElementById("searchUserInput").dataset.webLinkId), selectedUserId);
//             };
//         } else {
//             user.style.display = "none";
//         }
//     });

//     if (input.length > 0 && hasResults) {
//         userList.style.display = "block";
//     } else {
//         userList.style.display = "none";
//     }
// }

function searchWebLinks() {
    let input = document.getElementById("searchWebLinksInput").value.toLowerCase();
    let links = document.querySelectorAll("#webLinkList li");

    let hasResults = false;

    links.forEach(link => {
        let name = link.querySelector("strong").textContent.toLowerCase();
        let category = link.textContent.toLowerCase(); // 전체 텍스트에서 카테고리 포함 여부 확인

        if (name.includes(input) || category.includes(input)) {
            link.style.display = "flex"; // ✅ 검색 결과 포함되면 표시
            hasResults = true;
        } else {
            link.style.display = "none"; // ❌ 포함되지 않으면 숨김
        }
    });

    // ✅ 검색어가 없을 경우 전체 목록 다시 표시
    if (input.trim() === "") {
        links.forEach(link => {
            link.style.display = "flex";
        });
    }
}


// ✅ 웹 링크 공유 기능
function shareWebLink(webLinkId, userId) {
    console.log(`📢 [DEBUG] 최종 공유 요청 - webLinkId: ${webLinkId}, userId: ${userId}`);

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
            fetchSharedWebLinks();
        }
    })
    .catch(error => console.error("❌ 공유 중 오류 발생:", error));
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
        .then(response => response.json())
        .then(data => {
            console.log("📢 API 응답 데이터:", data);

            let sharedWebLinkList = document.getElementById("sharedWebLinkList");
            if (!sharedWebLinkList) {
                console.error("❌ 오류: 공유받은 링크를 표시할 #sharedWebLinkList 요소를 찾을 수 없음!");
                return;
            }

            sharedWebLinkList.innerHTML = ""; // 기존 목록 초기화

            if (data.shared_links.length === 0) {
                sharedWebLinkList.innerHTML = "<p>공유받은 웹 링크가 없습니다.</p>";
                return;
            }

            data.shared_links.forEach(link => {
                let li = document.createElement("li");
                li.classList.add("shared-web-link");  // ✅ 스타일이 적용되도록 확인

                li.innerHTML = `
                    <div class="web-link-info">
                        <strong>${link.name}</strong> - 
                        <a href="${link.url}" target="_blank">${link.url}</a> 
                        <span class="shared-by">| 공유한 사용자: ${link.shared_by}</span>
                    </div>
                    <div class="web-link-buttons">
                        ${link.permission === "write" ? `
                            <button class="edit-btn" onclick="openSharedEditModal('${link.id}')" data-permission="${link.permission}">
                                수정
                            </button>
                        ` : ''}
                    </div>
                `;

                sharedWebLinkList.appendChild(li);
            });
        })
        .catch(error => console.error("❌ 공유 웹 링크 불러오기 실패:", error));
}







// ✅ 로그인 후 공유받은 웹 링크 자동 로드
document.addEventListener("DOMContentLoaded", function () {
    fetchSharedWebLinks();
});

function shareWebLink(webLinkId, userId) {
    let selectedUserId = parseInt(document.getElementById("searchUserInput").dataset.selectedUserId);
    let permission = document.getElementById("sharePermission").value; // 🔹 선택한 권한 가져오기

    console.log(`📢 [DEBUG] 최종 공유 요청 - webLinkId: ${webLinkId}, userId: ${userId}, permission: ${permission}`);

    fetch("/feedmanager/share/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ webLinkId, userId: selectedUserId, permission: permission }) // ✅ 권한 함께 전송
    })
    .then(response => response.json())
    .then(data => {
        console.log("📢 서버 응답:", data);
        if (data.error) {
            alert("공유 실패: " + data.error);
        } else {
            alert("웹 링크가 공유되었습니다!");
            closeShareModal();
            fetchSharedWebLinks();
        }
    })
    .catch(error => console.error("❌ 공유 중 오류 발생:", error));
}


document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("shareAllBtn").addEventListener("click", openShareAllModal);
});

function openShareModal(webLinkId) {
    let shareModal = document.getElementById("shareModal");
    shareModal.style.display = "block";
    
    document.getElementById("searchUserInput").dataset.webLinkId = webLinkId;
    
    // ✅ 권한 선택 추가
    let permissionSelectHTML = `
        <label for="sharePermission">권한:</label>
        <select id="sharePermission">
            <option value="read">읽기</option>
            <option value="write">쓰기</option>
        </select>
    `;
    document.getElementById("shareModal").insertAdjacentHTML("beforeend", permissionSelectHTML);

    fetchUsers(webLinkId);
}


// ✅ ESC 키로 공유받은 웹 링크 수정 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeSharedEditModal();
    }
});


// ✅ ESC 키로 전체 공유 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeShareAllModal();
    }
});

// ✅ 전체 공유 모달 닫기
function closeShareAllModal() {
    document.getElementById("shareAllModal").style.display = "none";
}

function searchAllUsers() {
    let input = document.getElementById("searchAllUserInput").value.toLowerCase();
    let userList = document.getElementById("allUserList");
    let users = document.querySelectorAll("#allUserList li");

    let hasResults = false;

    // ✅ 검색어가 비어 있으면 리스트를 지우고 초기화 (다시 불러오기)
    if (input.length === 0) {
        userList.innerHTML = ""; // 목록 초기화
        userList.style.display = "none";
        fetchAllUsers(); // 사용자 목록 다시 불러오기
        return;
    }

    users.forEach(user => {
        let userText = user.dataset.username.toLowerCase();
        let userNameText = user.dataset.name.toLowerCase();
        let userEmailText = user.dataset.email.toLowerCase();

        if (
            userText.includes(input) ||
            userNameText.includes(input) ||
            userEmailText.includes(input)
        ) {
            user.style.display = "block";
            hasResults = true;
        } else {
            user.style.display = "none";
        }
    });

    // ✅ 검색 결과가 있으면 리스트 표시
    userList.style.display = hasResults ? "block" : "none";
}




// ✅ 모든 사용자 목록 불러오기
function fetchAllUsers() {
    return fetch("/users/all_users/")
        .then(response => response.json())
        .then(data => {
            let userList = document.getElementById("allUserList");
            userList.innerHTML = ""; // 목록 초기화
            userList.style.display = "none"; // 기본적으로 숨김

            data.users.forEach(user => {
                let li = document.createElement("li");
                li.dataset.userId = user.id;
                li.dataset.username = user.username || "";
                li.dataset.name = user.name || "";
                li.dataset.email = user.email || "";

                li.textContent = `${user.username} (${user.name}, ${user.email})`;

                li.onclick = function () {
                    console.log(`📢 [DEBUG] 선택된 사용자 - userId: ${li.dataset.userId}, username: ${li.dataset.username}`);

                    // ✅ 클릭된 사용자 음영 처리
                    highlightSelection(li);

                    // ✅ 선택한 사용자에게 전체 공유 실행
                    shareAllWebLinks(parseInt(li.dataset.userId));
                };

                userList.appendChild(li);
            });
        })
        .catch(error => console.error("❌ 전체 사용자 목록 불러오기 실패:", error));
}


function shareAllWebLinks(userId) {
    let confirmation = confirm("정말 모든 웹 링크를 이 사용자에게 공유하시겠습니까?");
    if (!confirmation) return;
    // ✅ 선택한 권한 가져오기
    let permission = document.getElementById("permissionSelect").value;
    console.log(`📢 [DEBUG] 전체 공유 요청: recipientId = ${userId}`);

    fetch("/feedmanager/share_all/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({ recipientId: userId, permission: permission })
    })
    .then(response => response.json())
    .then(data => {
        console.log("📢 [DEBUG] 서버 응답:", data);
        if (data.error) {
            alert("❌ 전체 공유 실패: " + data.error);
        } else {
            alert("✅ 모든 웹 링크가 성공적으로 공유되었습니다!");
            closeShareAllModal();
            fetchSharedWebLinks();
        }
    })
    .catch(error => console.error("❌ 전체 공유 중 오류 발생:", error));
}

function openShareAllModal() {
    let shareAllModal = document.getElementById("shareAllModal");

    if (!shareAllModal) {
        console.error("❌ 오류: #shareAllModal 요소를 찾을 수 없음!");
        return;
    }

    // ✅ 기존 `openShareModal`과 동일한 방식으로 설정
    shareAllModal.style.display = "block"; // 모달 열기
    document.getElementById("searchAllUserInput").value = ""; // 검색 입력 초기화
    fetchAllUsers(); // ✅ 전체 사용자 목록 불러오기
}

// ✅ 공유 모달 닫기
function closeShareAllModal() {
    let shareAllModal = document.getElementById("shareAllModal");
    if (!shareAllModal) return;
    shareAllModal.style.display = "none";
}

// ✅ ESC 키를 누르면 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeShareAllModal();
    }
});



// ✅ 공유받은 웹 링크 수정 모달 열기
function openSharedEditModal(webLinkId) {
    let modal = document.getElementById("sharedEditModal");

    if (!modal) {
        console.error("❌ 오류: sharedEditModal 요소를 찾을 수 없음!");
        return;
    }

    // ✅ 해당 웹 링크 데이터를 가져와서 모달에 채우기
    fetch(`/feedmanager/shared_link/${webLinkId}/`)
        .then(response => response.json())
        .then(data => {
            let editPermission = document.querySelector(`button[onclick="openSharedEditModal('${webLinkId}')"]`).dataset.permission;

            if (editPermission !== "write") {
                alert("❌ 수정 권한이 없습니다!");
                return;
            }

            document.getElementById("sharedEditWebLinkId").value = data.id;
            document.getElementById("sharedEditWebLinkName").value = data.name;
            document.getElementById("sharedEditWebLinkUrl").value = data.url;
            modal.style.display = "block";  // ✅ 모달 표시
        })
        .catch(error => console.error("❌ 공유된 웹 링크 데이터 불러오기 실패:", error));
}

// ✅ 공유받은 웹 링크 수정 모달 닫기
function closeSharedEditModal() {
    document.getElementById("sharedEditModal").style.display = "none";
}


// ✅ 공유받은 웹 링크 수정 요청 보내기
function editSharedWebLink() {
    let webLinkId = document.getElementById("sharedEditWebLinkId").value;
    let name = document.getElementById("sharedEditWebLinkName").value.trim();
    let url = document.getElementById("sharedEditWebLinkUrl").value.trim();

    if (!name || !url) {
        alert("수정할 웹 링크 이름과 URL을 입력하세요!");
        return;
    }

    fetch(`/feedmanager/edit_shared/${webLinkId}/`, {
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
            alert("✅ 공유받은 웹 링크가 수정되었습니다!");
            closeSharedEditModal();
            fetchSharedWebLinks(); // 목록 다시 불러오기
        }
    })
    .catch(error => console.error("❌ 공유받은 웹 링크 수정 중 오류 발생:", error));
}

// ✅ 공유받은 웹 링크 업데이트 (쓰기 권한이 있을 경우)
function updateSharedWebLink() {
    let webLinkId = document.getElementById("sharedEditWebLinkId").value;
    let name = document.getElementById("sharedEditWebLinkName").value.trim();
    let url = document.getElementById("sharedEditWebLinkUrl").value.trim();

    if (!name || !url) {
        alert("웹 링크 이름과 URL을 입력하세요!");
        return;
    }

    fetch(`/feedmanager/update_shared_link/${webLinkId}/`, {  // ✅ URL 확인
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
            alert("❌ 수정 실패: " + data.error);
        } else {
            alert("✅ 공유받은 웹 링크가 수정되었습니다!");
            closeSharedEditModal();
            fetchSharedWebLinks(); // ✅ 목록 새로고침
        }
    })
    .catch(error => console.error("❌ 공유받은 웹 링크 수정 중 오류 발생:", error));
}



// ✅ 공유받은 웹 링크 수정 모달 닫기
function closeSharedEditModal() {
    document.getElementById("sharedEditModal").style.display = "none";
}


// ✅ 클릭된 사용자 음영처리 효과 (클릭 후 색상 변경)
function highlightSelection(element) {
    let originalColor = element.style.backgroundColor; // 원래 색상 저장
    element.style.backgroundColor = "#d3d3d3"; // 클릭 시 회색 음영 처리
    setTimeout(() => {
        element.style.backgroundColor = originalColor || ""; // 원래 색상으로 복귀
    }, 500);
}




// ✅ window 객체에 삭제 함수 등록 (HTML에서 사용 가능하도록)
window.deleteWebLink = deleteWebLink;