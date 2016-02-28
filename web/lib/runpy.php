<!-- exec('./lib/image_to_midi.py') -->


$command = escapeshellcmd('./lib/image_to_midi.py');
$output = shell_exec($command);
echo $output;

