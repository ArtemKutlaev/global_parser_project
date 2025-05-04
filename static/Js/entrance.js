const error = document.getElementById('error');

async function CheckReg(el, event) {
  event.preventDefault();
  var login = el.text.value;
  var password = el.password.value;
  try {
    const response = await fetch('/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ login: login, password: password })
    });

    const data = await response.json();

    if (data.redirect_url) {
      window.location.href = data.redirect_url;
    } else {
      error.innerHTML = 'Неверный логин или пароль';
    }
  } catch (e) {
    error.innerHTML = `Ошибка: ${e.message}`;
  }
}
