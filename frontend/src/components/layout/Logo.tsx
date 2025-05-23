interface LogoProps {
  className?: string;
}

const Logo = ({ className = '' }: LogoProps) => {
  return (
    <svg className={className} viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Background */}
      <rect width="40" height="40" rx="8" fill="#0A2463"/>

      {/* Gradient overlay */}
      <rect width="40" height="40" rx="8" fill="url(#paint0_linear)" fillOpacity="0.2"/>

      {/* House shape */}
      <path d="M20 8L32 18V32H8V18L20 8Z" fill="#0E7C7B" stroke="white" strokeWidth="1.5"/>

      {/* Roof */}
      <path d="M20 8L32 18H8L20 8Z" fill="#14B8B6" stroke="white" strokeWidth="1.5"/>

      {/* Door */}
      <rect x="17" y="24" width="6" height="8" rx="1" fill="#0A2463" stroke="white" strokeWidth="1"/>

      {/* Window */}
      <rect x="12" y="20" width="5" height="5" rx="1" fill="#0A2463" stroke="white" strokeWidth="1"/>
      <rect x="23" y="20" width="5" height="5" rx="1" fill="#0A2463" stroke="white" strokeWidth="1"/>

      {/* Gradient definition */}
      <defs>
        <linearGradient id="paint0_linear" x1="0" y1="0" x2="40" y2="40" gradientUnits="userSpaceOnUse">
          <stop stopColor="white" stopOpacity="0.2"/>
          <stop offset="1" stopColor="white" stopOpacity="0"/>
        </linearGradient>
      </defs>
    </svg>
  );
};

export default Logo;
