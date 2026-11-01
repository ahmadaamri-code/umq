# يجمع مشاهد render_b.py بالترتيب ويضيف الصوت المولَّد → ep-trig-ferris.mp4
# الاستعمال من video-engine:  .\mux_ferris.ps1
$ErrorActionPreference = 'Stop'
$out = 'out_ferris'
$scenes = Get-ChildItem "$out\s*.mp4" | Where-Object { $_.Name -match '^s\d+\.mp4$' } | Sort-Object { [int]($_.BaseName.Substring(1)) }
$list = $scenes | ForEach-Object { "file '$($_.Name)'" }
Set-Content -Path "$out\list.txt" -Value $list -Encoding ascii
ffmpeg -y -loglevel error -f concat -safe 0 -i "$out\list.txt" -c copy "$out\video.mp4"
ffmpeg -y -loglevel error -i "$out\video.mp4" -i "$out\audio.wav" -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$out\ep-trig-ferris.mp4"
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of compact "$out\ep-trig-ferris.mp4"
