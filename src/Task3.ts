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

  classification(limits: PictureEnv, fileName: string): NewtonIterator {
    this.schedule.push([this.saveClassification, { limits, fileName }]);

    return this;
  }

  private getStatus(stage: Object[]) {
    if (stage[0] === this.saveSequence) {
      // @ts-ignore
      const zs = stage[1]['zs'];
      let line = zs.toString();
      if (line.length > 10) {
        line = line.slice(0, 10) + '...';
      }

      return new Sequence(
        `Sequence ${line}`,
        new Stage('Calculating', zs.length),
        new Stage('Saving', 1)
      );
    } else if (stage[0] === this.saveClassification) {
      // @ts-ignore
      const limits = stage[1]['limits'];

      return new Sequence(
        `Classification [${limits.lx}:${limits.rx}]` + `x[${limits.ly}:${limits.ry}]`
      );
    }

    throw new Error('Unexpected stage function');
  }

  run() {
    const stages = this.schedule.map(this.getStatus);
    // @ts-ignore
    this.status = new Sequence('All', stages).width(50);
    this.status.cachedPrint();

    for (let s of this.schedule) {
      s[0](s[1]);
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

      plt.scatter(x, y, linspace(50, 10, s.length), redGreenRange(s.length));
      plt.plot(x, y, 'o', (color = 'black'), (lw = 1), (ls = '-'), (ms = 1)); //bullshit.
      plt.plot(root.re, root.im, 'gh', (ms = 7)); //bullshit.

      if (this.status !== null) this.status.step();
    });

    plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', `${fileName}.png`)); //bullshit.
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
    plt.savefig(os.path.join(os.getcwd(), 'task3', 'out', `${fileName}.png`)); //bullshit.

    if (this.status !== null) this.status.step();
  }
}

function clear() {
  return undefined; // TODO.
}

class Reportable {
  private readonly width = 100;
  private readonly item = '-';
  public allTicks: number;
  public ticks: number;
  private readonly every: number;
  private cache: string;

  constructor(public name: string, public readonly limit: number) {
    this.allTicks = 0;
    this.ticks = 0;
    this.every = 1;
    this.cache = '';
  }

  private ensure(ticks: number | null, limit: number | null) {
    if (ticks === null) ticks = this.ticks;
    if (limit === null) limit = this.limit;

    return [ticks, limit];
  }

  protected bar(ticks: number | null = null, limit: number | null = null): string {
    [ticks, limit] = this.ensure(ticks, limit);
    const ratio = ticks / limit;
    const items = Math.floor(this.width * ratio);
    const empty = ratio === 1 ? '' : `>${' '.repeat(this.width - items - 1)}`;

    return `[${this.item.repeat(items)}${empty}] ${this.percent(ticks, limit)}`;
  }

  protected percent(ticks: number | null = null, limit: number | null = null): string {
    [ticks, limit] = this.ensure(ticks, limit);

    return `${Math.floor((100 * ticks) / limit)}%`;
  }

  protected ratio(ticks: number | null = null, limit: number | null = null): string {
    [ticks, limit] = this.ensure(ticks, limit);

    return `${ticks}/${limit}`;
  }

  tick(): boolean {
    if (!this.isFull()) {
      this.allTicks++;
      this.ticks++;

      return true;
    }

    return false;
  }

  protected cachedPrint() {
    // @ts-ignore
    const out = this.repr();

    if (out != this.cache && (this.allTicks % this.every == 0 || this.isFull())) {
      this.cache = out;
      clear();
      console.log(out);
    }
  }

  isFull(): boolean {
    return this.allTicks == this.fullLimit();
  }

  step() {
    if (this.tick()) this.cachedPrint();
  }

  // TODO setters for width and every.

  fullLimit() {
    return this.limit;
  }
}

class Stage extends Reportable {
  constructor(public readonly name: string, limit: number) {
    super(name, limit);
  }

  repr(): string {
    return `${this.name}:\n${this.bar()}\n`;
  }
}

class Iteration extends Reportable {
  public readonly origin: Reportable;
  private rep?: Reportable;

  constructor(limit: number, rep: Reportable) {
    super('Iteration', limit);
    this.ticks++;
    this.origin = rep;
    this.newRep();
  }

  private newRep(): void {
    this.rep = JSON.parse(JSON.stringify(this.origin));
    this.rep!.name += ` #${this.ticks}`;
  }

  tick(): boolean {
    if (this.rep!.tick()) this.allTicks++;
    if (!this.isFull()) {
      this.ticks++;
      this.newRep();

      return this.tick();
    }

    return false;
  }

  fullLimit(): number {
    return this.limit * this.rep!.fullLimit();
  }

  private repr() {
    return `${this.name} ${this.ratio()}:\n$${this.rep}`;
  }
}

class Sequence extends Reportable {
  private readonly stages: Reportable[];
  private readonly allLimit: number;

  constructor(name: string, ...args: Reportable[]) {
    super(name, args.length - 1);
    this.stages = args;
    this.allTicks = 0;
    this.allLimit = this.fullLimit();
  }

  private stage(): Reportable {
    return this.stages[this.ticks];
  }

  private nextStage(): boolean {
    if (!this.isFull()) {
      this.ticks++;
      return true;
    }

    return false;
  }

  tick(): boolean {
    if (this.stage().tick()) {
      this.allTicks++;

      if (this.stage().isFull()) {
        this.nextStage();
      }

      return true;
    }

    return this.nextStage() && this.tick();
  }

  fullLimit(): number {
    let sum = 0;
    this.stages.forEach(stage => {
      sum += stage.fullLimit();
    });

    return sum;
  }

  private repr(): string {
    return (
      `${this.name} (step ${this.ratio(this.ticks + 1, this.limit + 1)}):\n` +
      `${this.bar(this.allTicks, this.allLimit)}\n` +
      this.stages
        .slice(0, this.ticks + 1)
        .map(stage => {
          stage.toString();
        })
        .join()
    );
  }
}
