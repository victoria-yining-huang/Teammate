<?php
    header('Content-Type: application/json');
    setlocale(LC_CTYPE, "en_US.UTF-8");
    ini_set ( "set_time_limit" , "0" );

    $aResult = array();

    if( !isset($_POST['functionname']) ) { $aResult['error'] = 'No function name!'; }

    if( !isset($_POST['arguments']) ) { $aResult['error'] = 'No function arguments!'; }

    if( !isset($aResult['error']) ) {

        switch($_POST['functionname']) {

            case 'generate':
                $args = $_POST['arguments'];
                $students = escapeshellarg($args["students"] );
                $conflicts = escapeshellarg($args["conflicts"]);
                $team_size = escapeshellarg($args["team_size"]);
                $command = escapeshellcmd('python3 python/model.py ' . $students .' '. $conflicts .' '. $team_size);
                exec($command, $out, $status);
                $aResult['result'] = $out;
                break;

            default:
               $aResult['error'] = 'Not found function '.$_POST['functionname'].'!';
               break;
        }

    }

    echo json_encode($aResult);

?>