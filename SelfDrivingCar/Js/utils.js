function getIntersection(A, B, C, D) {
  const tTop = (D.x - C.x) * (A.y - C.y) - (D.y - C.y) * (A.x - C.x);
  const uTop = (C.y - A.y) * (A.x - B.x) - (C.x - A.x) * (A.y - B.y);
  const bottom = (D.y - C.y) * (B.x - A.x) - (D.x - C.x) * (B.y - A.y);

  if (bottom != 0) {
    const t = tTop / bottom;
    const u = uTop / bottom;
    if (t >= 0 && t <= 1 && u >= 0 && u <= 1) {
      return {
        x: A.x + t * (B.x - A.x),
        y: A.y + t * (B.y - A.y),
        offset: t,
      };
    }
  }

  return null;
}


function lerp(A,B,t){
    return A+(B-A)*t;
}

function polysIntersect(poly1, poly2) {
  for (let i = 0; i < poly1.length; i++) {
    const nextIndex = (i + 1) % poly1.length;
    const edge1Start = poly1[i];
    const edge1End = poly1[nextIndex];

    for (let j = 0; j < poly2.length; j++) {
      const nextJIndex = (j + 1) % poly2.length;
      const edge2Start = poly2[j];
      const edge2End = poly2[nextJIndex];

      if (getIntersection(edge1Start, edge1End, edge2Start, edge2End)) {
        return true;
      }
    }
  }
  return false;
}

function getRGBA(value){
    const alpha=Math.abs(value);
    const R=value<0?0:255;
    const G=R;
    const B=value>0?0:255;
    return "rgba("+R+","+G+","+B+","+alpha+")";
}

function getRandomColor(){
    const hue=290+Math.random()*260;
    return "hsl("+hue+", 100%, 60%)";
}