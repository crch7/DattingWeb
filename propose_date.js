body {
    font-family: Arial, sans-serif;
    background-color: #f4f4f4;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

h1 {
    color: #333;
}

.profile-container {
    width: 80%;
    max-width: 800px;
    margin: 30px auto;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-field {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #ddd;
}

.profile-field label {
    font-weight: bold;
    color: #555;
}

.profile-field span {
    color: #333;
}

.propose-date-link {
    text-align: center;
    margin-top: 20px;
}

.propose-date-link a {
    text-decoration: none;
    background-color: #FF4081;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background-color 0.3s;
}

.propose-date-link a:hover {
    background-color: #d02a61;
}

.notification {
    margin: 10px auto;
    padding: 10px;
    background-color: #ffeb3b;
    color: #333;
    font-weight: bold;
    border-radius: 5px;
    width: 80%;
    max-width: 600px;
    text-align: center;
}

.notification.success {
    background-color: #4caf50;
    color: white;
}

.notification.error {
    background-color: #f44336;
    color: white;
}

.profile-container img {
    max-width: 200px;
    max-height: 200px;
    width: auto;
    height: auto;
    object-fit: contain;
    border-radius: 5px;
    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.like-button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
}

.like-button {
    width: 80px;
    height: 80px;
    border: none;
    border-radius: 50%;
    background-color: #f0f0f0;
    color: #ccc;
    font-size: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
}

.like-button:hover {
    transform: scale(1.1);
}

.like-button.liked {
    background-color: #ff6961;
    color: white;
}

.like-button:not(.liked):hover {
    background-color: #ffe0e0;
}

.block-button-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 20px 0;
}

.block-button {
    width: 80px;
    height: 80px;
    border: none;
    border-radius: 50%;
    background-color: #f0f0f0;
    color: #ccc;
    font-size: 36px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transition: background-color 0.3s ease, color 0.3s ease, transform 0.2s ease;
}

.block-button:hover {
    transform: scale(1.1);
}

.block-button.blocked {
    background-color: #333;
    color: white;
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}

.block-button:not(.blocked):hover {
    background-color: #dcdcdc;
    color: #666;
}

.buttons-container {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin: 20px 0;
}

.like-button-container,
.block-button-container {
    display: flex;
    align-items: center;
    justify-content: center;
}

.additional-photos-gallery {
    text-align: center;
    margin: 20px 0;
}

.thumbnails {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin-bottom: 15px;
}

.thumbnail-button {
    border: none;
    background: none;
    padding: 0;
    cursor: pointer;
    transition: transform 0.2s;
}

.thumbnail-button:hover {
    transform: scale(1.1);
}

.thumbnail-image {
    width: 50px;
    height: 50px;
    object-fit: cover;
    border-radius: 5px;
    border: 2px solid transparent;
    transition: border-color 0.2s;
}

.thumbnail-button:hover .thumbnail-image,
.thumbnail-button:focus .thumbnail-image {
    border-color: #007bff;
}

.selected-photo-container {
    margin-top: 10px;
}

.selected-photo {
    width: auto;
    height: 400px;
    border-radius: 10px;
    border: 2px solid #ddd;
}
