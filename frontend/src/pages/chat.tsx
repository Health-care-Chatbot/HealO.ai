import { GradientHeading } from "@/components/ui/gradient-heading";
import { Thread } from "@/components/chat/thread";
import { AiInput } from "@/components/chat/ai-input";
export default function Chat() {
  return (
    <>
      <div className="flex flex-col max-w-[48rem] w-[60%] min-w-[24rem] mx-auto h-screen">
        <header className="bg-background px-4 py-3 flex items-center justify-between">
          <GradientHeading size={"xs"} variant={"secondary"}>
            HealO.ai
          </GradientHeading>
        </header>
        <Thread />
        <AiInput />
      </div>
    </>
  );
}
