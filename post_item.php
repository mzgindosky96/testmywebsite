<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $conn = new mysqli("localhost", "root", "", "market_db");
    
    // File upload handling
    $target_dir = "uploads/";
    $target_file = $target_dir . uniqid() . basename($_FILES["item_image"]["name"]);
    move_uploaded_file($_FILES["item_image"]["tmp_name"], $target_file);

    // Insert into database
    $stmt = $conn->prepare("INSERT INTO items (name, description, price, secret_code, image_path) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("ssiss", $_POST["item_name"], $_POST["item_description"], $_POST["item_price"], $_POST["secret_code"], $target_file);
    $stmt->execute();
    
    header("Location: index.php");
    exit();
}
?>