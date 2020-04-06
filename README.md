# DDreshape
DDreshape is program written in [Python](https://www.python.org/) for reshaping existing [Dungeondraft](https://dungeondraft.net/) maps. Dungeondraft is a map making tool for fantasy role-playing games. As of writing this, Dungeondraft is still in beta, and as such, [include bugs](https://www.reddit.com/r/dungeondraft/comments/f9wh5y/known_bugs_report_a_bug/) and some planned functionality is missing.
Reshaping (such as resizing or cropping) the map, after it has been created, is an [expected and anticipated funtionality](https://www.reddit.com/r/dungeondraft/comments/fcpn0a/is_there_any_method_for_resizing_a_map/), but it has not yet been inplemented in Dungeodraft.

The purpose of DDreshape is to fill the gap between current alpha/beta state of Dungeondraft and the final release, where reshaping is implemented in Dungeondraft.

DDreshape lets you pad, crop, rotate and flip your existing Dungeondraft maps.

# Examples
|Action|Command|Exported map|
|---|---|---|
|Input map||<img src="Examples/example_map.png" width="500px">|
|Padding|`--pad 1 2 3 4`|<img src="Examples/example_map__DDreshape__pad_1_2_3_4.png" width="500px">|
|Cropping|`--crop 1 2 3 4`|<img src="Examples/example_map__DDreshape__crop_1_2_3_4.png" width="500px">|
|Flip left-right|`--fliplr`|<img src="Examples/example_map__DDreshape__flip_lr.png" width="500px">|
|Flip up-down|`--flipud`|<img src="Examples/example_map__DDreshape__flip_ud.png" width="500px">|
|Transpose (flip diagonally)|`--transpose`|<img src="Examples/example_map__DDreshape__transpose.png" height="500px">|
|Rotate 90|`--rot90`|<img src="Examples/example_map__DDreshape__rot90.png" height="500px">|
