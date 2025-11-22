/**
 * Distance Value Object
 * 거리 표현 (km 단위)
 */

export class Distance {
  constructor(public readonly kilometers: number) {
    if (kilometers < 0) {
      throw new Error('Distance cannot be negative');
    }
  }
  
  toMeters(): number {
    return this.kilometers * 1000;
  }
  
  equals(other: Distance): boolean {
    return this.kilometers === other.kilometers;
  }
}

