import { GradientHeading } from "@/components/ui/gradient-heading";
import { motion } from "framer-motion";
import { TopShadow } from "@/components/ui/top-shadow";
import { Button } from "@/components/ui/button";
import { MoveRight } from "lucide-react";
import { useNavigate } from "react-router-dom";
import { initiateConversationUrl } from "@/lib/endpoints";
import axios from "axios";
import { useState } from "react";
import { useChatStore } from "@/store/chat-store";

export default function Home() {
  const containerVariants = {
    initial: { opacity: 0 },
    animate: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.5,
      },
    },
  };
  const childVariants = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
  };

  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const { addBubble } = useChatStore();

  const initiateChat = async () => {
    setIsLoading(true);
    const res = await axios.get(initiateConversationUrl);
    const { conversation, user_id } = res.data;
    localStorage.setItem("user_id", user_id);
    addBubble({
      sender: "ai",
      data: {
        isLoading: false,
        response: conversation,
      },
    });
    setIsLoading(false);
    navigate("/chat");
  };

  return (
    <div className="h-screen w-full flex justify-center items-center">
      <TopShadow />
      <motion.div
        className="flex flex-col items-center gap-2"
        variants={containerVariants}
        initial="initial"
        animate="animate"
      >
        <motion.div
          className="flex flex-col items-center gap-1 mb-2"
          variants={childVariants}
        >
          <GradientHeading variant={"secondary"} size={"xs"} weight={"bold"}>
            Welcome to
          </GradientHeading>
          <GradientHeading variant={"secondary"} size={"xxl"} weight={"bold"}>
            HealO.ai
          </GradientHeading>
        </motion.div>
        <motion.div className="mb-6" variants={childVariants}>
          <p className="text-xl font-medium tracking-tight">
            Your personalized AI health companion
          </p>
        </motion.div>
        <motion.div variants={childVariants}>
          <Button
            className="rounded-full tracking-tight"
            variant={"expandIcon"}
            size={"lg"}
            Icon={MoveRight}
            iconPlacement="right"
            onClick={initiateChat}
            disabled={isLoading}
          >
            Get Started
          </Button>
        </motion.div>
      </motion.div>
    </div>
  );
}
