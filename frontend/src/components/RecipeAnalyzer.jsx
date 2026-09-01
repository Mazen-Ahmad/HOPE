import React from 'react';
import { Loader2, Brain, AlertCircle, RouteIcon } from 'lucide-react';

const RecipeAnalyzer = ({ 
  recipeText, 
  setRecipeText, 
  loading, 
  error, 
  handleSubmit 
}) => {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 py-10 sm:py-20">
      <div className="w-full max-w-3xl">
        
        <div className="relative group">
          <div className="absolute -inset-px bg-gradient-to-b from-white/10 to-white/5 rounded-2xl blur-sm opacity-60" />
          
          <div className="relative bg-white/[0.02] backdrop-blur-xl border border-white/10 rounded-2xl p-4 sm:p-6 lg:p-8 xl:p-12">
            
            <div className="space-y-6 sm:space-y-8">
              
              <div className="text-center">
                <h2 className="text-2xl sm:text-3xl font-light text-white mb-3 sm:mb-4">
                  Enter Your Finance Query
                </h2>
                <p className="text-white/60 font-light text-sm sm:text-base">
                  Ask anything — single or multi-part finance questions
                </p>
              </div>
              
              <div className="space-y-4">
                <div className="relative">
                  <textarea
                    value={recipeText}
                    onChange={(e) => setRecipeText(e.target.value)}
                    placeholder="e.g. What is our net profit margin and can you update the pricing for Gold Credit Card?"
                    className="w-full h-48 sm:h-56 lg:h-64 px-4 sm:px-6 py-4 sm:py-6 bg-white/[0.03] backdrop-blur-sm border border-white/10 rounded-xl 
                             focus:border-white/20 focus:bg-white/[0.05] transition-all duration-300 
                             resize-none text-white/90 placeholder-white/40 text-sm sm:text-base leading-relaxed
                             outline-none shadow-inner"
                    disabled={loading}
                  />
                  
                  <div className="absolute bottom-3 sm:bottom-4 right-4 sm:right-6 flex flex-col sm:flex-row items-end sm:items-center space-y-2 sm:space-y-0 sm:space-x-4">
                    <div className="text-white/40 text-xs sm:text-sm font-light">
                      {recipeText.length} characters
                    </div>
                    {recipeText.length > 10 && (
                      <div className="text-emerald-400/60 text-xs sm:text-sm font-light flex items-center">
                        <AlertCircle className="w-3 h-3 sm:w-4 sm:h-4 mr-1" />
                        <span>Ready</span>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {error && (
                <div className="bg-red-500/10 backdrop-blur-sm border border-red-400/20 text-red-300 px-4 sm:px-6 py-3 sm:py-4 rounded-xl">
                  <div className="flex items-center">
                    <div className="w-2 h-2 bg-red-400 rounded-full mr-3 flex-shrink-0" />
                    <span className="font-light text-sm sm:text-base">{error}</span>
                  </div>
                </div>
              )}

              <button
                onClick={handleSubmit}
                disabled={loading || !recipeText.trim()}
                className="group relative w-full overflow-hidden bg-white/15 hover:bg-white/25 backdrop-blur-2xl text-white font-light py-4 sm:py-6 px-6 sm:px-8 rounded-2xl disabled:opacity-30 disabled:cursor-not-allowed transition-all duration-700 transform hover:scale-[1.01] disabled:hover:scale-100 flex items-center justify-center text-base sm:text-lg border border-white/25 hover:border-white/40"
              >
                <div className="relative flex items-center">
                  {loading ? (
                    <>
                      <Loader2 className="w-5 h-5 sm:w-6 sm:h-6 mr-3 sm:mr-4 animate-spin" />
                      <span className="text-sm sm:text-base">Routing Query...</span>
                    </>
                  ) : (
                    <>
                      <Brain className="w-5 h-5 sm:w-6 sm:h-6 mr-3 sm:mr-4 group-hover:scale-110 transition-transform duration-500" />
                      <span>Route Query</span>
                    </>
                  )}
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default RecipeAnalyzer;
