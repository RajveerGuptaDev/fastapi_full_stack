const BASE_URL = "https://fastapi-full-stack-3.onrender.com";


/* =====================
   SIGNUP FUNCTION
===================== */
async function signup() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    alert("Please fill all fields");
    return;
  }
                                                             
  const response = await fetch(`${BASE_URL}/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });                                                           

  const data = await response.json();

  // ❌ username exists or other error
  if (!response.ok) {
    alert(data.detail || "Signup failed");
    return;
  }

  // ✅ AUTO LOGIN AFTER SIGNUP
  localStorage.setItem("token", data.access_token);

  alert(`Welcome ${data.username}\nCharacter: ${data.employee_name}`);

  // 🚀 DIRECT PROFILE PAGE
  window.location.href = "profile.html";
}

/* =====================
   LOGIN FUNCTION
===================== */
async function login() {
  const username = document.getElementById("username").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!username || !password) {
    alert("Please fill all fields");
    return;
  }

  const response = await fetch(`${BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ username, password })
  });

  const data = await response.json();

  if (response.ok) {
    localStorage.setItem("token", data.access_token);
    window.location.href = "profile.html";
  } else {
    alert(data.detail || "Invalid credentials");
  }
}
