.profile-container {
    font-family: Arial, sans-serif;
    background-color: #fff;
    margin: 20px auto;
    padding: 20px;
    max-width: 800px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.profile-field {
    margin-bottom: 15px;
    word-wrap: break-word;
}

.profile-field label {
    font-weight: bold;
    color: #333;
    display: block;
    margin-bottom: 5px;
}

.profile-field span {
    font-size: 16px;
    color: #666;
    display: block;
    white-space: pre-wrap;
    overflow-wrap: break-word;
    word-break: break-word;
    max-width: 100%;
}

.profile-container img {
    max-width: 200px;
    height: auto;
    border-radius: 50%;
    display: block;
    margin: 20px auto;
    object-fit: cover;
}

.profile-field h3 {
    font-size: 18px;
    font-weight: bold;
    color: #333;
    margin-top: 20px;
}

.profile-field ul {
    list-style: none;
    padding-left: 0;
    margin-top: 10px;
}

.profile-field li {
    margin-bottom: 8px;
}

.profile-field a {
    color: #FF4081;
    text-decoration: none;
    font-size: 16px;
}

.profile-field a:hover {
    text-decoration: underline;
    color: #d02a61;
}

.profile-field span:empty {
    color: #ccc;
    font-style: italic;
}

.photo-gallery {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
}

.photo-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

.photo-thumbnail {
    width: 100px;
    height: 100px;
    object-fit: cover;
    border-radius: 5px;
    border: 1px solid #ddd;
}

.delete-button-container {
    margin-top: 5px;
}

.delete-button {
    width: 30px;
    height: 30px;
    background-color: #ff4d4d;
    color: white;
    border: none;
    border-radius: 5px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    font-size: 18px;
    transition: background-color 0.3s, transform 0.2s;
}

.delete-button:hover {
    background-color: #e00000;
    transform: scale(1.1);
}

.upload-button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #7e8083;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-weight: bold;
    font-size: 16px;
    transition: background-color 0.3s, transform 0.2s;
}

.upload-button:hover {
    background-color: #2d2e30;
    transform: scale(1.05);
}

.upload-submit-button {
    display: inline-block;
    padding: 10px 20px;
    background-color: #FF4081;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    margin-top: 10px;
    transition: background-color 0.3s, transform 0.2s;
}

.upload-submit-button:hover {
    background-color: #cc285f;
    transform: scale(1.05);
}

#file-name {
    font-style: italic;
    color: #555;
    font-size: 14px;
}
