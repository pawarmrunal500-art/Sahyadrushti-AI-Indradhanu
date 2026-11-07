import React, { useState, useEffect } from 'react';

interface SafeImageProps extends React.ImgHTMLAttributes<HTMLImageElement> {
  fallbackSrc?: string;
  badge?: string;
}

export const SafeImage: React.FC<SafeImageProps> = ({
  src,
  alt,
  fallbackSrc = '/sahyadri_landscape.jpg',
  className,
  style,
  badge,
  ...props
}) => {
  const [currentSrc, setCurrentSrc] = useState<string>(src || fallbackSrc);
  const [loaded, setLoaded] = useState<boolean>(false);
  const [hasError, setHasError] = useState<boolean>(false);

  useEffect(() => {
    setCurrentSrc(src || fallbackSrc);
    setHasError(false);
  }, [src, fallbackSrc]);

  return (
    <div style={{ position: 'relative', width: '100%', height: '100%', overflow: 'hidden' }}>
      <img
        src={hasError ? fallbackSrc : currentSrc}
        alt={alt || 'Sahyadri Geospatial Intelligence'}
        loading="lazy"
        onLoad={() => setLoaded(true)}
        onError={() => {
          if (!hasError) {
            setHasError(true);
            setCurrentSrc(fallbackSrc);
          }
        }}
        className={className}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
          display: 'block',
          transition: 'transform 0.35s ease, opacity 0.3s ease',
          opacity: loaded ? 1 : 0.85,
          ...style
        }}
        {...props}
      />
      {badge && (
        <span style={{
          position: 'absolute',
          bottom: '8px',
          left: '8px',
          background: 'rgba(15, 23, 42, 0.75)',
          backdropFilter: 'blur(4px)',
          color: '#ffffff',
          fontSize: '0.68rem',
          fontWeight: 600,
          padding: '2px 8px',
          borderRadius: '4px',
          pointerEvents: 'none'
        }}>
          {badge}
        </span>
      )}
    </div>
  );
};

export default SafeImage;

