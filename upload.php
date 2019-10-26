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


		// check if file is a .csv
		//echo $ext;
		if ($ext != "csv") {
			// *** change this to link to upload conflict error page ***
			echo "Sorry, file format is not a .CSV. Please try again.";
		} else {
			// Check if file already exists
			if (file_exists($path_filename_ext)) {
				// *** change this to link to file name already exists error page *** 
				echo "Sorry, file already exists.";
			} else {
				move_uploaded_file($temp_name,$path_filename_ext);
				header("Location: http://localhost:8888/conflict-file-success.html");
		 	}	
		}
	} else {
		// *** replace with file was not uploaded error page ***
		echo "A file was not uploaded. Please try again";
	}

?>

