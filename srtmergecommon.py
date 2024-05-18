import srt  # for srt format handling
import sys  # input arguments


def do_merge (primary_path, 
              primary_preamble, 
              primary_color,
              secondary_path, 
              secondary_preamble,
              secondary_color, 
              merged_path):

    # Read files and convert to list

    primary_file = open(primary_path, 'r', encoding='utf-8', errors='ignore')
    primary_text = primary_file.read()
    primary_file.close()
    secondary_file = open(secondary_path, 'r', encoding='utf-8',  errors='ignore')
    secondary_text = secondary_file.read()
    secondary_file.close()
    subtitle_generator_primary = srt.parse(primary_text)
    subtitles_primary = list(subtitle_generator_primary)
    subtitle_generator_secondary = srt.parse(secondary_text)
    subtitles_secondary = list(subtitle_generator_secondary)

    # Make primary color and position
    for s in subtitles_primary:
        s.content = f'{primary_preamble}<font color="{primary_color}">{s.content}</font>'

    # Make secondary color and position
    for s in subtitles_secondary:
        s.content = f'{secondary_preamble}<font color="{secondary_color}">{s.content}</font>'

    # Merge
    subtitles_merged = subtitles_primary + subtitles_secondary
    subtitles_merged = list(srt.sort_and_reindex(subtitles_merged))

    # Write merged to file
    #merged_path = primary_path.replace('.srt', '.merged.srt')
    merged_text = srt.compose(subtitles_merged)
    merged_file = open(merged_path, 'w', encoding='utf-8')
    merged_file.write(merged_text)
    merged_file.close()

