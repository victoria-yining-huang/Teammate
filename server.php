<?php
    header('Content-Type: application/json');

    $aResult = array();

    if( !isset($_POST['functionname']) ) { $aResult['error'] = 'No function name!'; }

    //if( !isset($_POST['arguments']) ) { $aResult['error'] = 'No function arguments!'; }

    if( !isset($aResult['error']) ) {

        switch($_POST['functionname']) {
            case 'add':
               if( !is_array($_POST['arguments']) || (count($_POST['arguments']) < 2) ) {
                   $aResult['error'] = 'Error in arguments!';
               }
               else {
                   $aResult['result'] = add(floatval($_POST['arguments'][0]), floatval($_POST['arguments'][1]));
               }
               break;

            case 'ping':
                $aResult['result'] = "Hey";
                $var = "Hello!";
                $command = escapeshellcmd('python3 python/model_mamp.py');
                exec($command, $out, $status);
                $aResult['result'] = $out[2];
                //$output = shell_exec('python /python/model.py' . $var);
                //$aResult['result'] = $output;
                break;

            default:
               $aResult['error'] = 'Not found function '.$_POST['functionname'].'!';
               break;
        }

    }

    echo json_encode($aResult);

?>