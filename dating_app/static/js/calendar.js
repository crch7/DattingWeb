body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
}

header {
    text-align: center;
    margin-top: 10px;
}

h1 a {
    color: #FF4081;
    text-decoration: none;
    font-size: 36px;
}

h1 a:hover {
    color: #c00a4a;
}

main {
    text-align: center;
    margin: 20px auto;
    padding: 20px;
    max-width: 800px;
}

footer {
    text-align: center;
    margin-top: 20px;
    padding: 10px;
    background-color: #fff;
    border-top: 1px solid #ddd;
}

footer nav {
    margin-top: 10px;
}

footer nav a {
    margin: 0 15px;
    text-decoration: none;
    color: #FF4081;
    font-weight: bold;
}

.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    height: 100vh;
    width: 200px;
    background-color: #FF4081;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
    border-radius: 0;
    overflow-y: auto;
}

.top-nav a {
    color: #fff;
    padding: 15px;
    text-decoration: none;
    border-bottom: 1px solid #333;
    transition: background-color 0.3s;
}

.top-nav a:hover {
    background-color: #c00a4a;
}

.top-nav a.active {
    background-color: #fff;
    color: #FF4081;
    font-weight: bold;
}

.user-profile {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 10px;
    margin-top: 10px;
    position: fixed;
    top: 0;
    right: 0;
    background-color: #fff;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    z-index: 1000;
}

.user-profile img.user-photo {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
}

.user-profile .user-photo-placeholder {
    width: 40px;
    height: 40px;
    background-color: #ccc;
    color: white;
    text-align: center;
    line-height: 40px;
    border-radius: 50%;
    font-size: 14px;
    margin-right: 10px;
}

.user-profile .user-name {
    margin-right: 10px;
    font-weight: bold;
    text-decoration: none;
    color: #333;
}

.user-profile .user-name:hover {
    color: #FF4081;
}

.user-profile .logout-button {
    padding: 5px 10px;
    background-color: #FF4081;
    color: #fff;
    border: none;
    border-radius: 5px;
    text-decoration: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.user-profile .logout-button:hover {
    background-color: #c00a4a;
}

.footer p {
    font-size: 16px;
    margin-bottom: 10px;
}

.footer .footer-links {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.footer .footer-link {
    color: rgb(0, 0, 0);
    text-decoration: none;
    font-size: 14px;
    transition: color 0.3s ease;
}

.footer .footer-link:hover {
    color: #FF4081;
    text-decoration: underline;
}
