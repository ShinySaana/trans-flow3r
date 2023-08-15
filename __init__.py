from st3m.application import Application, ApplicationContext
from st3m.input import InputState
from ctx import Context
import st3m.run
import leds

TRANS_FLAG_COLORS = [
    (91, 206, 250),
    (245, 169, 184),
    (255, 255, 255),
    # (245, 169, 184),
    # (91, 206, 250),
]

TRANS_FLAG_COLORS_NORMALIZED = [(r/255, g/255, b/255) for r, g, b in TRANS_FLAG_COLORS]

MIN_X = -120
MIN_Y = -120

LENGTH_X = 240
LENGTH_Y = 240

def draw_rectangle(ctx, color, start_x, start_y, width_x, width_y):
    ctx.rgb(*color).rectangle(start_x + MIN_X, start_y + MIN_Y, width_x, width_y).fill()

class Trans(Application):
    def __init__(self, app_ctx: ApplicationContext) -> None:
        super().__init__(app_ctx)
        self.counter = 0

    def draw(self, ctx: Context) -> None:
        ctx.rgb(0, 0, 0).rectangle(-120, -120, 240, 240).fill()
        current = self.counter
        self.counter += 1

        current_color = TRANS_FLAG_COLORS[current % len(TRANS_FLAG_COLORS)]
        current_led = current % 40

        leds.set_rgb(current_led, *current_color)
        leds.update()

        stripes = 3
        y_step = LENGTH_Y // stripes

        for i in range(stripes):
            y_start = (current + y_step * i) % 240
            draw_rectangle(ctx, TRANS_FLAG_COLORS_NORMALIZED[i], 0, y_start, LENGTH_X, y_step)

            if y_start + y_step > LENGTH_Y:
                overflowed_by = y_start + y_step - LENGTH_Y
                draw_rectangle(ctx, TRANS_FLAG_COLORS_NORMALIZED[i], 0, 0, LENGTH_X, overflowed_by)

    def think(self, ins: InputState, delta_ms: int) -> None:
        pass

if __name__ == '__main__':
    st3m.run.run_view(Trans(ApplicationContext()))
