import typing

class XY(typing.NamedTuple):
    x: int
    y: int

class Stroke(typing.NamedTuple):
    start: XY
    end: XY
class LineWriter:
    def __init__(self, origin, scale, text):
        from sims4.math import Vector3
        self.origin = origin
        self.step = Vector3(1, 0, 0)
        self.text = text
        self.scale = scale
        self.char_widths = {
            '.': Vector3(0.2, 0, 0)
        }
        self.char_strokes = {
            '1': [
                Stroke(XY(0.2, 0.7), XY(0.5, 1)),
                Stroke(XY(0.5, 0), XY(0.5, 1)),
                Stroke(XY(0.8, 0), XY(0.2, 0)),
            ],
            '2': [
                Stroke(XY(0.2, 0.8), XY(0.55, 1)),
                Stroke(XY(0.55, 1), XY(0.75, 0.5)),
                Stroke(XY(0.75, 0.5), XY(0.15, 0)),
                Stroke(XY(0.15, 0), XY(0.8, 0)),
            ],
            '3': [
                Stroke(XY(0.1, 0.8), XY(0.40, 1)),
                Stroke(XY(0.40, 1), XY(0.80, 0.6)),
                Stroke(XY(0.80, 0.6), XY(0.5, 0.5)),
                Stroke(XY(0.80, 0.4), XY(0.5, 0.5)),
                Stroke(XY(0.40, 0), XY(0.80, 0.4)),
                Stroke(XY(0.1, 0.2), XY(0.4, 0)),
            ],
            '4': [
                Stroke(XY(0.3, 1), XY(0.1, 0.5)),
                Stroke(XY(0.1, 0.5), XY(0.9, 0.55)),
                Stroke(XY(0.8, 1), XY(0.78, 0)),
            ],
            '5': [
                Stroke(XY(0.25, 0.9), XY(0.2, 0.7)),
                Stroke(XY(0.25, 0.9), XY(0.8, 0.9)),
                Stroke(XY(0.2, 0.7), XY(0.60, 0.6)),
                Stroke(XY(0.6, 0.6), XY(0.8, 0.35)),
              	Stroke(XY(0.65, 0.0), XY(0.8, 0.35)),
              	Stroke(XY(0.65, 0.0), XY(0.4, 0.04)),
              	Stroke(XY(0.2, 0.24), XY(0.4, 0.04)),
            ],
            '6': [
              	Stroke(XY(0.6, 0.6), XY(0.15, 0.5)),
                Stroke(XY(0.6, 0.6), XY(0.8, 0.3)),
              	Stroke(XY(0.6, 0.0), XY(0.8, 0.3)),
              	Stroke(XY(0.6, 0.0), XY(0.3, 0.04)),
              	Stroke(XY(0.15, 0.24), XY(0.3, 0.04)),
              	Stroke(XY(0.15, 0.24), XY(0.1, 0.5)),
              	Stroke(XY(0.1, 0.5), XY(0.3, 0.8)),
              	Stroke(XY(0.5, 0.9), XY(0.3, 0.8)),
              	Stroke(XY(0.5, 0.9), XY(0.8, 0.85)),
            ],
            '7': [
                Stroke(XY(0.1, 0.88), XY(0.7, 0.90)),
                Stroke(XY(0.7, 0.9), XY(0.4, 0)),
              	Stroke(XY(0.4, 0.5), XY(0.7, 0.52)),
            ],
            '8': [
                Stroke(XY(0.8, 0.8), XY(0.7, 0.88)),
                Stroke(XY(0.7, 0.88), XY(0.5, 0.9)),
              	Stroke(XY(0.5, 0.9), XY(0.2, 0.88)),
              	Stroke(XY(0.2, 0.88), XY(0.13, 0.8)),
              	Stroke(XY(0.13, 0.8), XY(0.1, 0.7)),
              	Stroke(XY(0.1, 0.7), XY(0.2, 0.6)),
              	Stroke(XY(0.2, 0.6), XY(0.5, 0.50)),
                Stroke(XY(0.5, 0.5), XY(0.7, 0.45)),
                Stroke(XY(0.7, 0.45), XY(0.8, 0.35)),
                Stroke(XY(0.8, 0.35), XY(0.83, 0.25)),
                Stroke(XY(0.83, 0.25), XY(0.8, 0.08)),
              	Stroke(XY(0.8, 0.08), XY(0.6, 0.03)),
              	Stroke(XY(0.6, 0.03), XY(0.45, 0.0)),
              	Stroke(XY(0.45, 0.0), XY(0.15, 0.1)),
                Stroke(XY(0.77, 0.78), XY(0.1, 0.15))
            ],
            '9': [
              	Stroke(XY(0.5, 0.5), XY(0.85, 0.5)),
                Stroke(XY(0.3, 0.9), XY(0.2, 0.7)),
              	Stroke(XY(0.3, 0.6), XY(0.2, 0.7)),
              	Stroke(XY(0.3, 0.9), XY(0.6, 0.96)),
                Stroke(XY(0.3, 0.6), XY(0.5, 0.5)),
              	Stroke(XY(0.85, 0.8), XY(0.6, 0.96)),
              	Stroke(XY(0.85, 0.8), XY(0.9, 0.5)),
              	Stroke(XY(0.9, 0.5), XY(0.8, 0.2)),
              	Stroke(XY(0.76, 0.1), XY(0.8, 0.2)),
              	Stroke(XY(0.76, 0.1), XY(0.55, 0)),
                Stroke(XY(0.35, 0.03), XY(0.55, 0)),
            ],
            '0': [
                Stroke(XY(0.8, 0.8), XY(0.7, 0.88)),
                Stroke(XY(0.7, 0.88), XY(0.5, 0.95)),
              	Stroke(XY(0.5, 0.95), XY(0.2, 0.88)),
              	Stroke(XY(0.2, 0.88), XY(0.13, 0.8)),
              	Stroke(XY(0.13, 0.8), XY(0.1, 0.5)),
              	Stroke(XY(0.1, 0.5), XY(0.1, 0.2)),
                Stroke(XY(0.1, 0.2), XY(0.15, 0.1)),
                Stroke(XY(0.83, 0.25), XY(0.8, 0.8)),
                Stroke(XY(0.83, 0.25), XY(0.8, 0.08)),
              	Stroke(XY(0.8, 0.08), XY(0.6, 0.03)),
              	Stroke(XY(0.6, 0.03), XY(0.45, 0.0)),
              	Stroke(XY(0.45, 0.0), XY(0.15, 0.1)),
                Stroke(XY(0.67, 0.78), XY(0.2, 0.15))
            ],
            'x': [
                Stroke(XY(0.75, 0.8), XY(0.25, 0)),
                Stroke(XY(0.75, 0), XY(0.25, 0.8)),
            ],
            'y': [
                Stroke(XY(0.75, 0.8), XY(0.55, 0)),
                Stroke(XY(0.68, 0.5), XY(0.25, 0.8)),
            ],
            'z': [
                Stroke(XY(0.25, 0.8), XY(0.75, 0.8)),
                Stroke(XY(0.75, 0.8), XY(0.25, 0)),
                Stroke(XY(0.25, 0), XY(0.75, 0)),
            ],
            '.': [
                Stroke(XY(0.1, 0.2), XY(0.2, 0.1)),
                Stroke(XY(0.2, 0.1), XY(0.1, 0.0)),
				Stroke(XY(0.1, 0.2), XY(0.0, 0.1)),
                Stroke(XY(0.0, 0.1), XY(0.1, 0.0)),
            ],
        }
    def write(self, drawlayer):
        from sims4.math import Vector3
        line_origin = self.origin
        char_origin = self.origin
        for i in range(len(self.text)):
            if self.text[i] == "\n":
                line_origin = line_origin + (Vector3(0, -1.2, 0) * self.scale)
                char_origin = line_origin
                continue
            self._write_char(drawlayer, self.text[i], char_origin)
            char_origin = char_origin + self._char_to_step(self.text[i])
    def _char_to_step(self, c):
        if c in self.char_widths:
            return self.char_widths[c] * self.scale
        else:
            return self.step * self.scale
    def _char_to_strokes(self, c):
        if c in self.char_strokes:
            return self.char_strokes[c]
        else: 
            # default to a square
            return [
                Stroke(XY(0, 0), XY(1, 0)),
                Stroke(XY(1, 0), XY(1, 1)),
                Stroke(XY(1, 1), XY(0, 1)),
                Stroke(XY(0, 1), XY(0, 0)),
                Stroke(XY(1, 1), XY(0, 0)),
                Stroke(XY(1, 0), XY(0, 1)),
            ]

        
    def _write_char(self, drawlayer, c, char_origin):
        from sims4.math import Vector3
        for s in self._char_to_strokes(c):
            start_vec3 = char_origin + (Vector3(s.start.x, s.start.y, 0) * self.scale)
            end_vec3 = char_origin + (Vector3(s.end.x, s.end.y, 0) * self.scale)
            drawlayer.add_segment_absolute(start_vec3, end_vec3)