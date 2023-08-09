
// js/script.js

document.addEventListener("DOMContentLoaded", function() {
    const logo = document.getElementById("logo");
    const dataDiv = document.getElementById("data");

    logo.addEventListener("click", function() {
        fetch("/api/get_data")  // 将 URL 替换为您的 API 接口地址
        .then(response => response.json())
        .then(data => {
            // 更新页面上的数据
            dataDiv.innerHTML = `<p>Data from API:</p><pre>${JSON.stringify(data, null, 2)}</pre>`;
        })
        .catch(error => {
            console.error("Error fetching data:", error);
        });
    });
});

