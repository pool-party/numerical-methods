import { Complex, complex } from 'mathjs';

/**
 * Returns squared distance between two complex numbers.
 * @param {Complex} z1 first complex number
 * @param {Complex} z2 second complex number
 * @returns {Number} squared distance between numbers.
 */
function squaredDistance(z1: Complex, z2: Complex): number {
  return Math.pow(z1.re - z2.re, 2) + Math.pow(z1.im - z2.im, 2);
}

/**
 * Tuple of 3 number values for color representation.
 */
type Color = [number, number, number];

/**
 * Converts tuple with hsv color to rgb values.
 * @param {Color} color hsv color to convert
 * @returns {Color} rgb tuple
 */
function hsvToRgb(color: Color): Color {
  const [h, s, v] = color;
  if (s === 0) return [v, v, v];

  const i = Math.floor(h * 6.0);
  const f = h * 6.0 - i;
  const p = v * (1.0 - s);
  const q = v * (1.0 - s * f);
  const t = v * (1.0 - s * (1.0 - f));

  switch (i % 6) {
    case 0:
      return [v, t, p];
    case 1:
      return [q, v, p];
    case 2:
      return [p, v, t];
    case 3:
      return [p, q, v];
    case 4:
      return [t, p, v];
    case 5:
      return [v, p, q];
  }

  return [-1, -1, -1];
}

/**
 *  Takes amount of colors and returns rgb array.
 * @param {number} size amount of colors
 * @returns {Color[]} array of rgb color values
 */
function distinctPalette(size: number): Color[] {
  const hsv: Color[] = [];
  for (let i = 0; i < size; i++) hsv.push([i / size, 0.5, 0.5]);

  return hsv.map(color => {
    return hsvToRgb(color);
  });
}

/**
 * //TODO.
 */
export class PictureEnv {
  public readonly colors: Color[];
  public readonly rx: number;
  public readonly ry: number;

  constructor(
    public readonly lx: number,
    public readonly ly: number,
    rx: number | null = null,
    ry: number | null = null,
    public readonly px = 1000,
    public readonly py = 1000,
    c = 3
  ) {
    this.rx = rx !== null ? rx : Math.abs(lx);
    this.ry = ry !== null ? ry : Math.abs(ly);

    this.colors = distinctPalette(c);
  }

  width(): number {
    return this.rx - this.lx;
  }

  height(): number {
    return this.ry - this.ly;
  }
}

/**
 * //TODO.
 */
export class Plane {
  public static readonly eps = 1e-10;
  public static readonly Eps = 1e10;
  private id: number;

  constructor(
    public readonly roots: Complex[],
    public readonly transformers: ((foo: Complex) => Complex)[]
  ) {
    this.id = 0;
  }

  selectTransformer(tid: number): Plane {
    this.id = tid;

    return this;
  }

  transform(z: Complex): Complex {
    return this.transformers[this.id](z);
  }

  check(z: Complex): number | null {
    const dists: number[] = [];
    for (const root of this.roots) dists.push(squaredDistance(z, root));

    for (let i = 0; i < dists.length; i++) {
      if (dists[i] < Plane.eps) return i;
    }

    for (let i = 0; i < dists.length; i++) {
      if (dists[i] < Plane.Eps) return null;
    }

    return -1;
  }
}

/**
 * Shows whether complex number is equal to zero.
 * @param {Complex} z number to check
 * @returns {boolean} is number a zero
 */
function isZero(z: Complex): boolean {
  return z.re === z.im && z.re === 0;
}

/**
 * Take 'number' and range, returns array with those borders equally divided
 * on 'number' of parts.
 * @param {number} start left border
 * @param {number} end right border
 * @param {number} step step between values of array
 * @returns {number[]} array of 'size' length
 */
function linspace(start: number, end: number, step: number): number[] {
  if (step === 1) {
    return [start, end];
  }

  const gap = (start - end) / (step - 1);
  const gaps: number[] = [];

  for (let sum = 0; sum < end; sum += gap) {
    gaps.push(sum);
  }

  return gaps;
}

/**
 * Returns red-green palette as an array
 * @param {number} size amount of colors
 * @returns {Color[]} array of colors
 */
function redGreenRange(size: number): Color[] {
  const r = linspace(1, 0, size);
  const g = linspace(0, 1, size);

  const range: Color[] = [];
  for (let i = 0; i < size; i++) {
    range.push([r[i], g[i], 0]);
  }

  return range;
}

type IterationProduct = [Complex[], number];
type Schedule = [any, Object];

export class NewtonIterator {
  public status: any | null;
  public readonly schedule: Schedule[];

  constructor(public readonly plane: Plane) {
    this.status = null;
    this.schedule = [];
  }

  newtonIterations(z: Complex): IterationProduct {
    const sequence = [z];
    while (this.plane.check(z) === null) {
      if (isZero(z)) return [sequence, -1];

      z = this.plane.transform(z);
      sequence.push(z);
    }

    return [sequence, this.plane.check(z)!];
  }

  sequence(z: Complex | any, limits: PictureEnv, fileName: string): NewtonIterator {
    this.schedule.push([this.saveSequence, { zs: [z], limits, fileName }]);

    return this;
  }

  classification(limits: PictureEnv, fileName: string) {
    this.schedule.push([this.saveClassification, { limits, fileName }]);

    return this;
  }

  private getStatus(stage: Object[]) {
    if (stage[0] === this.saveSequence) {
      const zs = stage[1]['zs'];
      let line = zs.toString();
      if (line.length > 10) {
        line = line.slice(0, 10) + '...';
      }

      return Sequence(undefined); // TODO.
    } else if (stage[0] === this.saveClassification) {
      const limits = stage[1]['limits'];

      return Sequence(undefined); // TODO.
    }
  }

  run() {
    const stages = undefined; // TODO.
    this.status = Sequence('All', stages).width(50); // TODO.
    this.status.getAttribute('_cached_print')(); // wtf is this.

    for (let s of this.schedule) {
      s[0](s[1]); // wtf is this.
    }

    this.status = null;
  }

  // All plt operations are not real!!!
  private saveSequence(zs: Complex[], limits: PictureEnv, fileName: string) {
    plt.figure();
    plt.axis('equal');
    plt.xlim(limits.lx, limits.rx);
    plt.ylim(limits.ly, limits.ry);

    zs.forEach(z => {
      const [s, k] = this.newtonIterations(z);
      const [x, y] = s.map(zz => {
        return [zz.re, zz.im];
      });
      const root = this.plane.roots[k];

      plt.scatter(x, y, linspace(50, 10, s.length), redGreenRange(s.length)); //idk.
      plt.plot(x, y, 'o', (color = 'black'), (lw = 1), (ls = '-'), (ms = 1)); //bullshit.
      plt.plot(root.re, root.im, 'gh', (ms = 7)); //bullshit.

      if (this.status !== null) this.status.step();
    });

    plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', `f${fileName}.png`)); //bullshit.
    if (this.status !== null) this.status.step();
  }

  // All plt operations are not real!!!
  private saveClassification(limits: PictureEnv, fileName: string) {
    const [w, h] = [limits.width() * limits.px + 1, limits.height() * limits.py + 1];
    const roots = this.plane.roots.length;
    const points: Complex[][] = [];
    for (let i = 0; i <= roots; i++) {
      points.push([]);
    }

    for (let i = 0; i < w; i++) {
      for (let j = 0; j < h; j++) {
        const z = complex(
          limits.lx + (limits.width() * i) / w,
          limits.ly + (limits.height() * j) / h
        );
        const k = this.newtonIterations(z)[1];
        points[k].push(z);
      }

      if (this.status !== null) this.status.step();
    }

    plt.figure();
    plt.axis('equal');
    for (let i = 0; i <= roots; i++) {
      const [x, y] = points[i].map(z => {
        return [z.re, z.im];
      });
      plt.plot(x, y, 'o', (color = limits.colors[i]), (ms = 1)); //bullshit.
    }
    plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', `f${fileName}.png`)); //bullshit.

    if (this.status !== null) this.status.step();
  }
}
