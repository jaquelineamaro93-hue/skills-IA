import React from 'react';
import {Composition, Still} from 'remotion';
import timeline from './timeline.json';
import {Episode} from './compositions/Episode';
import {Thumbnail} from './compositions/Thumbnail';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition id="Camilo-Ep1-Vertical" component={Episode} durationInFrames={Math.round(timeline.duration * timeline.fps)} fps={timeline.fps} width={1080} height={1920} />
    <Still id="Camilo-Thumbnail" component={Thumbnail} width={1080} height={1920} />
  </>
);
