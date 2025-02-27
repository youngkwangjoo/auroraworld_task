document.addEventListener("DOMContentLoaded", function () {
    fetchWebLinks();
    fetchSharedWebLinks();
});

/* ==========================================
    공통 fetch 함수 (GET 요청)
========================================== */
function fetchData(url, callback) {
    fetch(url)
        .then(response => response.json())
        .then(data => callback(data))
        .catch(error => console.error(`❌ [ERROR] ${url}:`, error));
}

/* ==========================================
    웹 링크 목록 불러오기
========================================== */
function fetchWebLinks() {
    fetchData("/feedmanager/all_links/", data => {
        let webLinkList = document.getElementById("webLinkList");
        webLinkList.innerHTML = data.weblinks.length 
            ? data.weblinks.map(link => createWebLinkItem(link)).join("")
            : "<p>등록된 웹 링크가 없습니다.</p>";
    });
}

function createWebLinkItem(link) {
    return `
        <li class="web-link-item">
            <div class="web-link-info">
                <strong>${link.name}</strong> - 
                <a href="${link.url}" target="_blank">${link.url}</a> 
                (<span class="category">${link.category}</span>) <!-- ✅ span 태그 추가 -->
            </div>
            <div class="web-link-buttons">
                <button class="edit-btn" onclick="openEditModal(${link.id}, '${link.name}', '${link.url}')">수정</button>
                <button class="delete-btn" onclick="deleteWebLink(${link.id})">삭제</button>
            </div>
        </li>
    `;
}


/* ==========================================
    웹 링크 검색 기능
========================================== */
function searchWebLinks() {
    let input = document.getElementById("searchWebLinksInput").value.trim().toLowerCase();

    // 카테고리 변환 테이블 (하드코딩)
    const CATEGORY_MAP = {
        "personal": "개인 즐겨찾기",
        "work": "업무 활용 자료",
        "reference": "참고 자료",
        "education": "교육 및 학습 자료",
        "other": "기타"
    };

    document.querySelectorAll("#webLinkList li").forEach(link => {
        let name = link.querySelector("strong").textContent.trim().toLowerCase();
        let categoryElement = link.querySelector(".category");
        let categoryKey = categoryElement ? categoryElement.textContent.trim().toLowerCase() : "";
        let categoryName = Object.values(CATEGORY_MAP).find(c => c.includes(categoryKey)) || categoryKey;

        if (name.includes(input) || categoryName.includes(input)) {
            link.style.display = "flex";
        } else {
            link.style.display = "none";
        }
    });
}
/* ==========================================
    웹 링크 등록 기능
========================================== */
//  "등록하기" 버튼 클릭 이벤트 추가
document.addEventListener("DOMContentLoaded", function () {
    let addWebLinkBtn = document.getElementById("addWebLinkBtn");
    if (addWebLinkBtn) {
        addWebLinkBtn.addEventListener("click", openAddWebLinkModal);
    }
});

// 웹 링크 등록 모달 열기
function openAddWebLinkModal() {
    let modal = document.getElementById("addWebLinkModal");
    if (modal) {
        modal.style.display = "block";
    }
}

// 웹 링크 등록하기
function addWebLink() {
    let nameInput = document.getElementById("webLinkName").value.trim();
    let urlInput = document.getElementById("webLinkUrl").value.trim();
    let categoryInput = document.getElementById("webLinkCategory").value;

    if (!nameInput || !urlInput) {
        alert("웹 링크 이름과 URL을 입력하세요!");
        return;
    }

    fetch("/feedmanager/add/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()
        },
        body: JSON.stringify({
            name: nameInput,
            url: urlInput,
            category: categoryInput
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("등록 실패: " + data.error);
        } else {
            alert(" 웹 링크가 등록되었습니다!");
            closeAddWebLinkModal();
            fetchWebLinks(); 
        }
    })
    .catch(error => console.error("❌ 등록 중 오류 발생:", error));
}

// ESC 키로 등록 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeAddWebLinkModal();
    }
});

// 웹 링크 등록 모달 닫기 함수
function closeAddWebLinkModal() {
    let modal = document.getElementById("addWebLinkModal");
    if (modal) {
        modal.style.display = "none";
    }
}


/* ==========================================
    ✅ 웹 링크 수정 기능
========================================== */
function openEditModal(id, name, url) {
    document.getElementById("editWebLinkId").value = id;
    document.getElementById("editWebLinkName").value = name;
    document.getElementById("editWebLinkUrl").value = url;
    document.getElementById("editModal").style.display = "block";
}

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        let editModal = document.getElementById("editModal");
        if (editModal && editModal.style.display === "block") {
            closeEditModal();
        }
    }
});

// 기존 closeEditModal() 함수 활용
function closeEditModal() {
    let modal = document.getElementById("editModal");
    if (modal) {
        modal.style.display = "none";
    }
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
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
        body: JSON.stringify({ name, url })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.error ? `수정 실패: ${data.error}` : "웹 링크가 수정되었습니다!");
        closeEditModal();
        fetchWebLinks();
    })
    .catch(error => console.error("Error:", error));
}

/* ==========================================
    웹 링크 삭제
========================================== */
function deleteWebLink(id) {
    if (!confirm("정말 삭제하시겠습니까?")) return;

    fetch(`/feedmanager/delete/${id}/`, {
        method: "DELETE",
        headers: { "X-CSRFToken": getCSRFToken() }
    })
    .then(response => response.json())
    .then(data => {
        alert(data.error ? `삭제 실패: ${data.error}` : "웹 링크가 삭제되었습니다!");
        fetchWebLinks();
    })
    .catch(error => console.error("❌ 삭제 중 오류 발생:", error));
}

/* ==========================================
    공유받은 웹 링크 목록 불러오기
========================================== */
function fetchSharedWebLinks() {
    fetchData("/feedmanager/shared_links/", data => {
        let sharedWebLinkList = document.getElementById("sharedWebLinkList");
        if (!sharedWebLinkList) return console.error("❌ [ERROR] 공유받은 링크를 표시할 요소 없음!");

        sharedWebLinkList.innerHTML = data.shared_links.length
            ? data.shared_links.map(link => createSharedWebLinkItem(link)).join("")
            : "<p>공유받은 웹 링크가 없습니다.</p>";
    });
}

function createSharedWebLinkItem(link) {
    return `
        <li class="shared-web-link">
            <div class="web-link-info">
                <strong>${link.name}</strong> - 
                <a href="${link.url}" target="_blank">${link.url}</a> 
                <span class="shared-by">| 공유한 사용자: ${link.shared_by}</span>
            </div>
            ${link.permission === "write" ? `
                <button class="edit-btn" onclick="openSharedEditModal('${link.id}')">수정</button>
            ` : ""}
        </li>
    `;
}

/* ==========================================
     공유 모달 기능
========================================== */
function openShareModal(webLinkId) {
    document.getElementById("shareModal").style.display = "block";
    document.getElementById("searchUserInput").dataset.webLinkId = webLinkId;
    fetchUsers(webLinkId);
}

function closeShareModal() {
    document.getElementById("shareModal").style.display = "none";
}

/* ==========================================
    전체 공유 기능
========================================== */
// 전체 공유 모달 열기
function openShareAllModal() {
    let shareAllModal = document.getElementById("shareAllModal");

    if (!shareAllModal) {
        console.error("❌ 오류: #shareAllModal 요소를 찾을 수 없음!");
        return;
    }

    shareAllModal.style.display = "block";  // 모달 열기
    document.getElementById("searchAllUserInput").value = "";  // 검색 입력 초기화
    fetchAllUsers();  //  전체 사용자 목록 불러오기
}

//  전체 공유 모달 닫기
function closeShareAllModal() {
    let shareAllModal = document.getElementById("shareAllModal");
    if (!shareAllModal) return;
    shareAllModal.style.display = "none";
}

//  ESC 키를 누르면 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeShareAllModal();
    }
});

//  전체 공유 실행 (모든 웹 링크를 특정 사용자에게 공유)
function shareAllWebLinks(userId) {
    let confirmation = confirm("정말 모든 웹 링크를 이 사용자에게 공유하시겠습니까?");
    if (!confirmation) return;

    //  선택한 권한 가져오기
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

//  모든 사용자 목록 불러오기
function fetchAllUsers() {
    return fetch("/users/all_users/")
        .then(response => response.json())
        .then(data => {
            let userList = document.getElementById("allUserList");
            userList.innerHTML = ""; 
            userList.style.display = "none";  

            data.users.forEach(user => {
                let li = document.createElement("li");
                li.dataset.userId = user.id;
                li.dataset.username = user.username || "";
                li.dataset.name = user.name || "";
                li.dataset.email = user.email || "";

                li.textContent = `${user.username} (${user.name}, ${user.email})`;

                li.onclick = function () {

                    highlightSelection(li);

                    shareAllWebLinks(parseInt(li.dataset.userId));
                };

                userList.appendChild(li);
            });
        })
        .catch(error => console.error("❌ 전체 사용자 목록 불러오기 실패:", error));
}

// 전체 사용자 검색
function searchAllUsers() {
    let input = document.getElementById("searchAllUserInput").value.toLowerCase();
    let userList = document.getElementById("allUserList");
    let users = document.querySelectorAll("#allUserList li");

    let hasResults = false;

    // 검색어가 비어 있으면 리스트를 지우고 초기화 (다시 불러오기)
    if (input.length === 0) {
        userList.innerHTML = "";  // 목록 초기화
        userList.style.display = "none";
        fetchAllUsers();  // 사용자 목록 다시 불러오기
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

    // 검색 결과가 있으면 리스트 표시
    userList.style.display = hasResults ? "block" : "none";
}

// ESC 키 입력 시 전체 공유 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeShareAllModal();
    }
});

// 공유 모달 버튼 이벤트 추가
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("shareAllBtn").addEventListener("click", openShareAllModal);
});

// window 객체에 등록 (HTML에서 `onclick`으로 호출 가능하도록)
window.openShareAllModal = openShareAllModal;
window.closeShareAllModal = closeShareAllModal;
window.shareAllWebLinks = shareAllWebLinks;
window.fetchAllUsers = fetchAllUsers;
window.searchAllUsers = searchAllUsers;

// 클릭된 사용자 음영처리 효과 (클릭 후 색상 변경)
function highlightSelection(element) {
    let originalColor = element.style.backgroundColor; 
    element.style.backgroundColor = "#d3d3d3"; 
    setTimeout(() => {
        element.style.backgroundColor = originalColor || ""; 
    }, 500);
}

// window 객체에 등록 (HTML에서 onclick으로 호출 가능하도록)
window.highlightSelection = highlightSelection;



/* ==========================================
    공유받은 웹 링크 수정 기능 
========================================== */
// 공유받은 웹 링크 수정 모달 열기
function openSharedEditModal(webLinkId) {
    fetch(`/feedmanager/shared_link/${webLinkId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById("sharedEditWebLinkId").value = data.id;
            document.getElementById("sharedEditWebLinkName").value = data.name;
            document.getElementById("sharedEditWebLinkUrl").value = data.url;
            document.getElementById("sharedEditModal").style.display = "block";
        })
        .catch(error => console.error("❌ 공유된 웹 링크 데이터 불러오기 실패:", error));
}

// 공유받은 웹 링크 수정 요청 보내기
function editSharedWebLink() {
    let webLinkId = document.getElementById("sharedEditWebLinkId").value;
    let name = document.getElementById("sharedEditWebLinkName").value.trim();
    let url = document.getElementById("sharedEditWebLinkUrl").value.trim();

    if (!name || !url) {
        alert("수정할 웹 링크 이름과 URL을 입력하세요!");
        return;
    }

    fetch(`/feedmanager/update_shared_link/${webLinkId}/`, {  
        method: "PUT",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCSRFToken() },
        body: JSON.stringify({ name, url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(`❌ 수정 실패: ${data.error}`);
        } else {
            alert(" 공유받은 웹 링크가 수정되었습니다!");
            closeSharedEditModal();
            fetchSharedWebLinks();
        }
    })
    .catch(error => console.error("❌ 공유받은 웹 링크 수정 중 오류 발생:", error));
}

// 공유받은 웹 링크 수정 모달 닫기
function closeSharedEditModal() {
    let modal = document.getElementById("sharedEditModal");
    if (modal) {
        modal.style.display = "none";
    } else {
        console.error("❌ sharedEditModal 요소를 찾을 수 없습니다.");
    }
}

// ESC 키 입력 시 공유받은 웹 링크 수정 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeSharedEditModal();
    }
});

// `window` 객체에 등록 (HTML에서 `onclick`으로 호출 가능하도록)
window.openSharedEditModal = openSharedEditModal;
window.editSharedWebLink = editSharedWebLink;
window.closeSharedEditModal = closeSharedEditModal;
window.updateSharedWebLink = editSharedWebLink;  


// 공유받은 웹 링크 수정 모달 닫기
function closeSharedEditModal() {
    let modal = document.getElementById("sharedEditModal");
    if (modal) {
        modal.style.display = "none";
    } else {
        console.error("❌ sharedEditModal 요소를 찾을 수 없습니다.");
    }
}

// ESC 키 입력 시 공유받은 웹 링크 수정 모달 닫기
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeSharedEditModal();
    }
});

// `window` 객체에 등록 (HTML에서 `onclick`으로 호출 가능하도록)
window.openSharedEditModal = openSharedEditModal;
window.editSharedWebLink = editSharedWebLink;
window.closeSharedEditModal = closeSharedEditModal;
window.updateSharedWebLink = editSharedWebLink; 


/* ==========================================
    ✅ CSRF 토큰 가져오기
========================================== */
function getCSRFToken() {
    return document.cookie.split("; ").find(row => row.startsWith("csrftoken="))?.split("=")[1] || "";
}

