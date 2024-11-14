'use client';

import cx from 'classnames';

interface LogoProps {
  includeBrandName?: boolean;
  hasCustomLogo?: boolean;
  style?: 'default' | 'grayscale' | 'coral';
  className?: string;
  darkModeEnabled?: boolean;
}

export const Logo: React.FC<LogoProps> = ({
  includeBrandName = true,
  hasCustomLogo,
  className,
  style = 'default',
  darkModeEnabled,
}) => {
  return (
    <img
      src={includeBrandName ? '/images/logo_with_name.png' : '/images/logo_without_name.png'}
      alt={includeBrandName ? 'Logo with brand name' : 'Logo'}
      className={cx('h-full', { 'w-24': includeBrandName, 'w-4': !includeBrandName }, className)}
    />
  );
};
