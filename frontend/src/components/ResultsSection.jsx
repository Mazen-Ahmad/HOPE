import React from 'react';
import { TrendingUp, Layers, ShoppingBag, BookOpen, BarChart2 } from 'lucide-react';

const agentConfig = {
  profitability_agent: {
    label: 'Profitability Agent',
    color: 'text-emerald-300',
    bg: 'bg-emerald-500/10',
    border: 'border-emerald-400/30',
    icon: TrendingUp,
  },
  liquidity_agent: {
    label: 'Liquidity Agent',
    color: 'text-blue-300',
    bg: 'bg-blue-500/10',
    border: 'border-blue-400/30',
    icon: Layers,
  },
  product_agent: {
    label: 'Product Agent',
    color: 'text-amber-300',
    bg: 'bg-amber-500/10',
    border: 'border-amber-400/30',
    icon: ShoppingBag,
  },
  knowledge_agent: {
    label: 'Knowledge Agent',
    color: 'text-purple-300',
    bg: 'bg-purple-500/10',
    border: 'border-purple-400/30',
    icon: BookOpen,
  },
};

const ResultsSection = ({ result, showResults }) => {
  const subQueries = result?.sub_queries || [];

  return (
    <section className="min-h-screen flex items-center justify-center px-4 sm:px-6 lg:px-8 py-10 sm:py-20">
      <div className={`w-full max-w-4xl transform transition-all duration-1000 ${showResults ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>

        <div className="relative">
          <div className="absolute -inset-px bg-gradient-to-b from-white/10 to-white/5 rounded-2xl blur-sm opacity-60" />

          <div className="relative bg-white/[0.02] backdrop-blur-xl border border-white/10 rounded-2xl p-4 sm:p-6 lg:p-8 xl:p-12">

            <div className="text-center mb-8 sm:mb-12">
              <h2 className="text-2xl sm:text-3xl lg:text-4xl font-light text-white mb-3">
                Routing Complete
              </h2>
              <p className="text-white/50 font-light text-sm sm:text-base">
                {subQueries.length} sub-{subQueries.length === 1 ? 'query' : 'queries'} detected
              </p>
            </div>

            <div className="space-y-4">
              {subQueries.map((item, i) => {
                const config = agentConfig[item.agent] || {
                  label: item.agent,
                  color: 'text-white/70',
                  bg: 'bg-white/5',
                  border: 'border-white/10',
                  icon: BarChart2,
                };
                const IconComponent = config.icon;
                const confidencePct = Math.round(item.confidence * 100);

                return (
                  <div
                    key={i}
                    className={`${config.bg} ${config.border} border rounded-2xl p-4 sm:p-6 backdrop-blur-xl`}
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div className="flex items-start gap-3 flex-1 min-w-0">
                        <div className={`mt-0.5 flex-shrink-0 w-8 h-8 rounded-xl flex items-center justify-center bg-white/10`}>
                          <IconComponent className={`w-4 h-4 ${config.color}`} />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-white/90 font-light text-sm sm:text-base leading-relaxed">
                            {item.query}
                          </p>
                          {item.extraction?.financial_terms?.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-2">
                              {item.extraction.financial_terms.map((term, j) => (
                                <span key={j} className="text-white/40 text-xs bg-white/5 border border-white/10 rounded-full px-2 py-0.5">
                                  {term}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>
                      </div>

                      <div className="flex-shrink-0 text-right">
                        <div className={`text-sm font-light ${config.color}`}>
                          {config.label}
                        </div>
                        <div className="text-white/40 text-xs mt-1">
                          {confidencePct}% confidence
                        </div>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      </div>
    </section>
  );
};

export default ResultsSection;
