import numpy as np
import regex as re
from functools import reduce


def image_permutations(image):
    output = np.empty((8, *image.shape)).astype(image.dtype)
    output[0] = image
    for i in range(3):
        output[i+1] = np.rot90(output[i])
    for i in range(4):
        output[4+i] = np.fliplr(output[i])
    return output


def image_side(image, side):
    if side == 0:
        return image[0]
    elif side == 1:
        return image[:, -1]
    elif side == 2:
        return image[-1]
    elif side == 3:
        return image[:, 0]


def find_match(all_permutations, image, side):
    image_perms = image_permutations(image)
    curr_side = image_side(image, side)
    for perm in all_permutations:
        if not any((perm == i).all() for i in image_perms) and (image_side(perm, (side+2) % 4) == curr_side).all():
            return perm
    return None


def solve1(images):
    all_images = {tile: image_permutations(image) for tile, image in images.items()}
    all_permutations = np.vstack(list(all_images.values()))
    fm = lambda image, side: find_match(all_permutations, image, side)
    corners = [
        tile for tile, image in images.items()
        if sum(fm(image, i) is not None for i in range(4)) == 2
    ]
    return reduce(lambda x, y: x * y, corners)


def solve2(images):
    all_images = {tile: image_permutations(image) for tile, image in images.items()}
    all_permutations = np.vstack(list(all_images.values()))
    fm = lambda image, side: find_match(all_permutations, image, side)
    corners = [
        tile for tile, image in images.items()
        if sum(fm(image, i) is not None for i in range(4)) == 2
    ]
    corner_tile = next(
        perm for perm in image_permutations(images[corners[0]])
        if (fm(perm, 2) is not None and fm(perm, 3) is not None)
    )

    def find_column(image, side):
        col = np.empty((12, *image.shape))
        col[0] = image
        for i in range(11):
            col[i+1] = fm(col[i], side)
        return col

    grid = [find_column(a, 3) for a in find_column(corner_tile, 2)]
    no_borders = np.array([np.array([j[1:-1, 1:-1] for j in i]) for i in grid])
    picture = np.vstack([np.hstack(i) for i in no_borders])

    spacing = '[.#\n]{77}'
    monster = f'#.{spacing + "#....#" * 3}##{spacing}.#{"..#" * 5}'
    for pic in image_permutations(picture):
        text = '\n'.join(''.join('#' if i else '.' for i in row) for row in pic)
        if n_mosters := len(re.findall(monster, text, overlapped=True)):
            return int(pic.sum().sum() - (15 * n_mosters))
    raise ValueError("WHERE IS THE DAMN MONSTER???")


if __name__ == "__main__":
    with open('../data/day20.txt', 'r') as f:
        data = {
            int(tile): (np.array([list(line) for line in image.split()]) == '#').astype(np.uint8)
            for tile, image in re.findall(r"Tile (\d+):\n([\.#\n]+)", f.read())
        }
    print(solve1(data))
    print(solve2(data))
