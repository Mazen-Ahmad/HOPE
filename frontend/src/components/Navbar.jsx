import React from 'react';
import { Brain } from 'lucide-react';

const Navbar = ({ navRef }) => {
  return (
    <nav
      ref={navRef}
      className="absolute top-0 left-0 right-0 z-50 p-4 sm:p-6 lg:p-8 transition-all duration-500 ease-in-out"
    >
      <div className="flex justify-between items-center">
        <div className="flex items-center space-x-2 sm:space-x-4">
          <div className="relative">
            <div className="absolute inset-0 bg-white/10 blur-lg rounded-full" />
            <div className="relative bg-black/20 backdrop-blur-xl border border-white/20 rounded-full p-2 sm:p-3">
              <Brain className="w-4 h-4 sm:w-6 sm:h-6 text-white" />
            </div>
          </div>
          <div className="text-white font-thick text-sm sm:text-lg lg:text-xl tracking-widest">HOPE</div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;