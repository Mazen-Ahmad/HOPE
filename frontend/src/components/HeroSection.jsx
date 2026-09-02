import React from 'react';
import { ArrowDown } from 'lucide-react';

const HeroSection = ({ animateHero }) => {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className={`text-center max-w-5xl mx-auto transition-all duration-2000 ${animateHero ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-12'}`}>
        
        <div className="mb-8 sm:mb-12 lg:mb-16">
          <h1 className="text-4xl sm:text-6xl lg:text-8xl font-script text-white/95 mb-4 sm:mb-6 lg:mb-8 tracking-widest leading-none px-2">
            Financial <span className="block sm:inline text-red-300">Query </span>Router
          </h1> 
        </div>
        


          <p className="text-lg sm:text-xl lg:text-2xl text-white/60 max-w-2xl mx-auto leading-relaxed mb-8 sm:mb-10 lg:mb-12 px-4">
          <span className="text-emerald-300 font-medium">Agent </span>{' '}
          picker model
        </p>
        
        <div className="animate-bounce mt-16 sm:mt-20 lg:mt-26">
          <div className="flex flex-col items-center space-y-1">
            <ArrowDown className="w-5 h-5 sm:w-6 sm:h-6 text-white/60" />
            <div className="text-white/40 text-xs sm:text-sm font-light tracking-widest">LET'S SEE</div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;