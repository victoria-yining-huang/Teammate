<?php

	if (($_FILES['my_file']['name']!="")){
		// Where the file is going to be stored
		 $target_dir = "conflict-files/";
		 $file = $_FILES['my_file']['name'];
		 $path = pathinfo($file);
		 $filename = $path['filename'];
		 $ext = $path['extension'];
		 $temp_name = $_FILES['my_file']['tmp_name'];
		 $path_filename_ext = $target_dir.$filename.".".$ext;


		move_uploaded_file($temp_name,$path_filename_ext);
		header("Location: http://localhost:8888/conflict-file-success.html");
	}

?>
