import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Send } from "lucide-react";
import { useChatStore } from "@/store/chat-store";

export function AiInput() {
  const { setUserInput, addBubble } = useChatStore();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const input = e.currentTarget.compose.value;
    addBubble({ sender: "user", data: input });
    setUserInput(input);
    e.currentTarget.reset();
  };

  return (
    <>
      <form onSubmit={handleSubmit}>
        <div className="bg-background bg-[radial-gradient(ellipse_50%_110%_at_50%_100%,rgba(120,119,198,0.3),rgba(255,255,255,0))] shadow-t px-4 py-3 flex justify-end items-center">
          <Input
            className="rounded-full text-xs bg-background/30 backdrop-blur-md"
            placeholder="Message HealO.."
            id="compose"
          />
          <Button
            type="submit"
            size={"icon"}
            variant={"gooeyRight"}
            className="absolute float-end rounded-full mr-1"
          >
            <Send className="w-4 h-4" />
          </Button>
        </div>
      </form>
    </>
  );
}
