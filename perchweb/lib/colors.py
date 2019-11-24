""" Nerdy color calculation stuff """


def rgbToHsl(r, g, b):
    """ Converts R, G, B (0-255) values to (H, S, L) (0-1.0) """
    r /= 255
    g /= 255
    b /= 255

    max_c = max(r, g, b)
    min_c = min(r, g, b)

    h = s = l = (max_c + min_c) / 2

    if max_c == min_c:
        # Grayscale
        h = s = 0
    else:
        d = max_c - min_c
        s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)

        if max_c == r:
            h = (g - b) / d + (6 if g < b else 0)
        elif max_c == g:
            h = (b - r) / d + 2
        else:
            h = (r - g) / d + 4

        h /= 6

    return (h, s, l)


def hue2rgb(p, q, t):
    """ part of hslToRgb algo """
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1/6:
        return p + (q - p) * 6 * t
    if t < 0.5:
        return q
    if t < 2/3:
        return p + (q - p) * (2/3 - t) * 6
    return p


def hslToRgb(h, s, l):
    """ Converts H, S, L (0-1.0) values to (R, G, B) (0-255) """
    r = g = b = None

    if s == 0:
        # Grayscale
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue2rgb(p, q, h + 1/3)
        g = hue2rgb(p, q, h)
        b = hue2rgb(p, q, h - 1/3)

    return (round(r * 255), round(g * 255), round(b * 255))


def hexToRgb(hex_string):
    """ #FC20A9 -> (252, 32, 169)"""
    hex_string = hex_string.lstrip('#')
    return tuple(int(hex_string[i:i+2], 16) for i in (0, 2, 4))


def rgbToHex(r, g, b):
    """ 142, 102, 30 -> #fc20a9 """
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)


def lighten(hex_color, amount):
    """ Lighten a given hex_color by a fixed amount 0-1.0 """
    rgb = hexToRgb(hex_color)
    hsl = rgbToHsl(rgb[0], rgb[1], rgb[2])
    light = max(min(hsl[2] + amount, 1), 0)
    rgb = hslToRgb(hsl[0], hsl[1], light)
    return rgbToHex(rgb[0], rgb[1], rgb[2])

# Could easily add saturation and make them optional but we're always and only doing light atm


def scale(hex_color, light_scale):
    """ Lighten a given hex_color by scale, 0.1 = 10% more light than before """
    rgb = hexToRgb(hex_color)
    hsl = rgbToHsl(rgb[0], rgb[1], rgb[2])
    light = max(min(hsl[2] * (1 + light_scale), 1), 0)
    rgb = hslToRgb(hsl[0], hsl[1], light)
    return rgbToHex(rgb[0], rgb[1], rgb[2])
