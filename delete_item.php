<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $conn = new mysqli("localhost", "root", "", "market_db");
    
    // Verify secret code
    $stmt = $conn->prepare("SELECT secret_code, image_path FROM items WHERE id = ?");
    $stmt->bind_param("i", $_POST["item_id"]);
    $stmt->execute();
    $item = $stmt->get_result()->fetch_assoc();
    
    if ($_POST["secret_code"] === $item["secret_code"]) {
        // Delete from database
        $stmt = $conn->prepare("DELETE FROM items WHERE id = ?");
        $stmt->bind_param("i", $_POST["item_id"]);
        $stmt->execute();
        
        // Delete image file
        unlink($item["image_path"]);
    }
    
    header("Location: index.php");
    exit();
}
?>