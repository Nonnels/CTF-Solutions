<?php
function generateRandomString($length = 12) {
    $characters = 'abcdefghijkmpqrstuvwxyzABCDEFGHJKLMPQRSTUVWXYZ23456789';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[mt_rand(0, $charactersLength - 1)];
    }
    return $randomString;
}
for($i=0;$i<10000000;$i++){
    mt_srand($i);
    print(generateRandomString(12)."\n");
    }
?>
