function addLink() {
    let linkInput = document.getElementById("webLink").value.trim();
    let nameInput = document.getElementById("webLinkName").value.trim();
    let categoryInput = document.getElementById("webLinkCategory").value;

    if (!linkInput || !nameInput) {
        alert("웹 링크와 이름을 입력하세요!");
        return;
    }

    fetch("/feedmanager/add/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // CSRF 토큰 포함
        },
        body: JSON.stringify({
            url: linkInput,
            name: nameInput,
            category: categoryInput
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert("등록 실패: " + data.error);
        } else {
            alert("웹 링크가 등록되었습니다!\n이름: " + data.name + "\nURL: " + data.url + "\n카테고리: " + data.category);
            document.getElementById("webLink").value = "";
            document.getElementById("webLinkName").value = "";
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
