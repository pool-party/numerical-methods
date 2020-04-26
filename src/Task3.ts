import { Complex } from "mathjs";

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

//TODO NewtonIterator class
