const error = document.getElementById('error');
async function CheckReg(el) {
  event.preventDefault();
  var login = el.text.value;
  var password = el.password.value;

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
    // Здесь можно добавить обработку ошибок, если redirect_url отсутствует
    error.innerHTML = 'Неверный логин или пароль';   
  }
}
