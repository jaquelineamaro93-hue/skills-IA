import {continueRender, delayRender, staticFile} from 'remotion';

const faces: [string, string, string, string][] = [
  ['Anton', 'anton-latin-400-normal.woff2', '400', 'normal'],
  ['Montserrat', 'montserrat-latin-500-normal.woff2', '500', 'normal'],
  ['Montserrat', 'montserrat-latin-700-normal.woff2', '700', 'normal'],
  ['Montserrat', 'montserrat-latin-800-normal.woff2', '800', 'normal'],
  ['Montserrat', 'montserrat-latin-500-italic.woff2', '500', 'italic'],
  ['Montserrat', 'montserrat-latin-700-italic.woff2', '700', 'italic'],
  ['Montserrat', 'montserrat-latin-800-italic.woff2', '800', 'italic'],
];

let loaded = false;
export const loadFonts = () => {
  if (loaded || typeof document === 'undefined') return;
  loaded = true;
  const h = delayRender('Carregando fontes');
  Promise.all(
    faces.map(([family, file, weight, style]) =>
      new FontFace(family, `url(${staticFile('fonts/' + file)})`, {weight, style})
        .load()
        .then((f) => (document.fonts as unknown as {add: (f: FontFace) => void}).add(f)),
    ),
  ).then(() => continueRender(h));
};
