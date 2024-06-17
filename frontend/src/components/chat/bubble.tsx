import { MarkdownFadeIn } from "@/components/ui/markdown-fade-in";
import { AiBubbleData } from "@/lib/types";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { promptUrl } from "@/lib/endpoints";
import { useChatStore } from "@/store/chat-store";
import axios from "axios";

export function UserBubble(props: { text: string }) {
  return (
    <div className="flex items-start justify-end gap-4">
      <div className="bg-primary rounded-lg p-3 max-w-[50%] min-w-[25%]">
        <div className="font-semibold text-sm tracking-tight">You</div>
        <div className="text-xs tracking-tight">
          <p>{props.text}</p>
        </div>
      </div>
    </div>
  );
}

export function AiBubble(props: { data: AiBubbleData }) {
  return (
    <div className="flex items-start gap-4 justify-start">
      <div className="bg-accent text-accent-foreground rounded-lg p-3 min-w-[30%] max-w-[70%]">
        <div className="font-bold text-foreground tracking-tight">HealO</div>
        <div className="text-xs flex flex-col gap-2 tracking-tight">
          {props.data.isLoading ? (
            <LoadingSkeleton />
          ) : (
            <>
              {props.data.response?.map((res, i) => {
                if (res.type === "Text") {
                  return (
                    <MarkdownFadeIn
                      markdown={res.body}
                      className="text-xs font-normal"
                      key={i}
                    />
                  );
                } else if (res.type === "Form") {
                  return <ChatForm fields={res.body} key={i} />;
                }
              })}
            </>
          )}
        </div>
      </div>
    </div>
  );
}

function ChatForm(props: { fields: object }) {
  const { addAiLoadingBubble, showAiResponse } = useChatStore();
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    // Preparing data to send
    const userId = localStorage.getItem("user_id");
    const formDataJson: { [key: string]: string } = {};
    Object.keys(props.fields).forEach((field) => {
      formDataJson[field] = e.currentTarget[field].value;
    });

    // Add loading bubble
    addAiLoadingBubble();

    // Fetching the data from the API and showing the response
    const res = await axios.post(promptUrl, {
      user_id: userId,
      type: "Form",
      body: formDataJson,
    });
    const { conversation } = res.data;
    showAiResponse(conversation);
  };
  return (
    <form onSubmit={handleSubmit}>
      <div className="flex flex-col gap-2 rounded-md py-2">
        {Object.keys(props.fields).map((field, i) => {
          const fieldName = field.split("_").join(" ");
          return (
            <div key={i}>
              <Label className="text-xs capitalize ml-1" htmlFor={field}>
                {fieldName}
              </Label>
              <Input
                className="text-xs"
                placeholder={`Enter your ${fieldName}`}
                id={field}
              />
            </div>
          );
        })}
        <Button type="submit" size={"sm"} className="text-xs mt-2">
          Submit
        </Button>
      </div>
    </form>
  );
}

function LoadingSkeleton() {
  return (
    <div
      role="status"
      className="animate-pulse space-y-2 w-40 mt-2 *:h-2 *:rounded-full *:bg-accent-foreground *:brightness-50"
    >
      <div className="w-[100%]"></div>
      <div className="w-[60%]"></div>
    </div>
  );
}
