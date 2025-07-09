import Link from "next/link";
import { FuturisticButton } from "@/components/common/FuturisticButton";
import { HolographicCard } from "@/components/common/HolographicCard";
import { GlassPanel } from "@/components/common/GlassPanel";
import {
  FiZap,
  FiMessageSquare,
  FiBarChart2,
  FiUsers,
  FiLock,
} from "react-icons/fi";

export default function HomePage() {
  const features = [
    {
      icon: <FiZap className="text-purple-400 text-2xl" />,
      title: "Instant Insights",
      description: "Get real-time business intelligence powered by AI",
    },
    {
      icon: <FiMessageSquare className="text-blue-400 text-2xl" />,
      title: "Natural Conversations",
      description: "Interact with your data using natural language",
    },
    {
      icon: <FiBarChart2 className="text-green-400 text-2xl" />,
      title: "Data Visualization",
      description: "Automatically generate charts and reports",
    },
    {
      icon: <FiUsers className="text-yellow-400 text-2xl" />,
      title: "Team Collaboration",
      description: "Share insights with your team seamlessly",
    },
    {
      icon: <FiLock className="text-red-400 text-2xl" />,
      title: "Enterprise Security",
      description: "Military-grade encryption for your data",
    },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-gray-900">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 z-0 opacity-20">
          <div className="absolute top-1/4 left-1/4 w-64 h-64 rounded-full bg-purple-600 filter blur-3xl opacity-70 animate-float" />
          <div className="absolute top-1/3 right-1/4 w-96 h-96 rounded-full bg-blue-600 filter blur-3xl opacity-50 animate-float delay-1000" />
          <div className="absolute bottom-1/4 left-1/2 w-80 h-80 rounded-full bg-indigo-600 filter blur-3xl opacity-60 animate-float delay-2000" />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 md:py-32">
          <div className="text-center">
            <h1 className="text-4xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 via-blue-400 to-purple-600 mb-6">
              Your AI Business Assistant
            </h1>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-10">
              Revolutionize your workflow with our cutting-edge AI assistant
              designed specifically for business professionals.
            </p>
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link href="/chat">
                <FuturisticButton size="lg">Start Chatting</FuturisticButton>
              </Link>
              <Link href="/demo">
                <FuturisticButton variant="outline" size="lg">
                  Live Demo
                </FuturisticButton>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <GlassPanel className="p-8">
          <h2 className="text-3xl font-bold text-center text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500 mb-12">
            Powerful Features
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((feature, index) => (
              <HolographicCard key={index} className="p-6 h-full">
                <div className="flex flex-col items-center text-center">
                  <div className="mb-4 p-3 rounded-full bg-gray-800/50 border border-gray-700">
                    {feature.icon}
                  </div>
                  <h3 className="text-xl font-semibold text-white mb-2">
                    {feature.title}
                  </h3>
                  <p className="text-gray-300">{feature.description}</p>
                </div>
              </HolographicCard>
            ))}
          </div>
        </GlassPanel>
      </section>

      {/* CTA Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24">
        <HolographicCard className="p-8 md:p-12 text-center">
          <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-blue-500 mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-gray-300 max-w-3xl mx-auto mb-8">
            Join thousands of professionals who are already leveraging AI to
            gain a competitive edge.
          </p>
          <div className="flex justify-center">
            <Link href="/signup">
              <FuturisticButton size="lg">Get Started Free</FuturisticButton>
            </Link>
          </div>
        </HolographicCard>
      </section>
    </div>
  );
}
