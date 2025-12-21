const BASE_URL = "http://127.0.0.1:8000";

/* ==========================
   PAGE LOAD HOTE HI RUN
========================== */
window.onload = function () {
  loadProfile();
};

/* ==========================
   LOAD PROFILE DATA
========================== */
async function loadProfile() {
  const token = localStorage.getItem("token");

  // 🔒 Token nahi mila → login page
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  const response = await fetch(`${BASE_URL}/me`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${token}`
    }
  });

if (response.status === 401) {
  alert("Session expired. Please login again.");
  localStorage.removeItem("token");
  window.location.href = "login.html";
  return;
}

if (!response.ok) {
  console.error("Profile fetch failed:", response.status);
  return;
}


  const data = await response.json();

  // 🧾 HTML me data fill karo
  document.getElementById("username").innerText = data.username;
  document.getElementById("character").innerText =
    "Character: " + data.character;
  document.getElementById("department").innerText =
    "Department: " + data.department;
  document.getElementById("salary").innerText =
    "Salary: ₹" + data.salary;
}

/* ==========================
   LOGOUT
========================== */
function logout() {
  localStorage.removeItem("token");
  window.location.href = "login.html";
}
