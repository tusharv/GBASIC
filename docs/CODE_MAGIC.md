# Code Magic with Ollama Cloud

Code Magic is Ghost BASIC's optional AI companion. Press **F8** or click **Magic** in
the editor to open the right-side assistant panel. Your code and output stay visible on
the right while you debug, explain, write or improve a BASIC program. Editing, execution,
examples and F1 help still work offline. Magic requires an internet connection and your
own Ollama Cloud account and API key; no local Ollama installation or model download is needed.

## First use

1. Create an API key at [Ollama settings](https://ollama.com/settings/keys).
2. Launch `GBASIC`, press **F8**, open **Settings**, and enter the key in the masked **API key** field.
3. Keep `gemma4:31b`, or enter another available name from
   [Ollama Cloud models](https://ollama.com/search?c=cloud), then choose **Use settings**.
4. Choose **Debug**, **Explain**, **Write**, or **Suggest**. Type a request, then **Send**.
   A blank request uses the selected action's example instruction.
5. Read **Answer**, inspect **Code**, and open **Changes** to review the full diff.
   **Apply** becomes available only after review and a successful local syntax check.
6. Applying writes directly into the current editor on the left and keeps Magic open. The change is unsaved. **Ctrl+Z** undoes it, **F5** runs it,
   and **F2** saves it when you are ready.

The key and model are retained only for the current app session after Use settings. Closing the
app forgets values entered in Settings. You can also supply `OLLAMA_API_KEY` and optional
`OLLAMA_MODEL` in the environment before launching; Ghost BASIC does not read `.env` files.
Avoid putting actual credentials in source files, screenshots or shell history.

For a hidden prompt in Bash/Zsh (activate your virtual environment first):

```sh
export OLLAMA_API_KEY="$(python -c 'import getpass; print(getpass.getpass("Ollama API key: "))')"
export OLLAMA_MODEL='gemma4:31b'
GBASIC
unset OLLAMA_API_KEY
```

Alternatively, use the masked in-app field on any platform. The Cloud API uses names
like `gemma4:31b`, not the local Ollama CLI's `:cloud` suffix. Models may change; the field
is editable. Available API names can be listed at `https://ollama.com/api/tags`.

## Useful requests

- **Debug:** “This fails when I enter zero. Explain why and add input validation.”
- **Write:** “Add a menu to choose between simple and compound interest. Keep my existing formulas.”
- **Write:** “Create a hollow triangle using nested FOR loops and explain each loop.”
- **Explain:** “Walk through the values of I and J for the first three iterations.”
- **Suggest:** “What exercise should I try next to understand arrays?”

Follow-up questions in the same panel retain up to three recent conversation turns.
Closing the panel clears the conversation. Changing Context also clears it, so turning
context off does not silently send an earlier program through chat history.

## What is sent and what the agent can do

Only an explicit **Send** contacts `https://ollama.com/api/chat`. **Context: ON** includes
this editor's source and the last 6,000 characters of output/error from a matching last
run, plus the request, recent panel history and Ghost BASIC's language constraints.
It does not browse other files or read your environment. **Context: OFF** excludes the
source and last-run output. The API key is an authentication header, not model context;
its exact value is redacted from prompts and responses if accidentally included.
Other secrets embedded in source are not automatically detected, so inspect what you share.

The agent proposes code, compiles it locally without running it, and can ask the model
for one correction if the check fails. At most two Cloud calls happen per Send. The
full request has a two-minute deadline; Cancel or Escape cancels local network activity.
Requests already sent may still count against your Ollama usage. No automatic retries
are made for authentication, connectivity or quota errors.

The assistant has no shell, filesystem, package installation or program execution tools.
It cannot save or run suggested code. The review compares the full replacement against
the editor snapshot, and refuses to overwrite a buffer changed since Send captured the source.
Network calls use TLS and do not follow redirects. Keys and chat history are not written
to disk by Ghost BASIC; process environment/session memory is not an OS credential vault.

## Limits and troubleshooting

- A local syntax check does **not** prove runtime correctness. Test generated code with F5,
  including boundary inputs. The assistant may still misunderstand the requested behavior.
- Ghost BASIC executes a numbered BASIC subset. The assistant is told about its supported
  statements and intrinsics; QBasic procedures, graphics and other planned features remain
  unavailable. See [compatibility](../COMPATIBILITY.md).
- Cloud context is limited to 60,000 source characters. Proposals are also limited to
  1,000 lines and 2,000 characters per line; responses are bounded to 128 KiB. Oversized
  source is rejected explicitly rather than silently sent as a partial program.
- Multiple, unclosed or unlabelled code blocks are not eligible for Apply. Ask for one
  complete numbered program in a `basic` code block.
- **API key/access error:** check the key and your account's Cloud access.
- **Model not found:** choose a current model from Ollama's list.
- **Usage limit:** check your Ollama plan/usage and try later.
- **Connection/timeout:** check internet access, try a smaller request or another model.
- **Program changed:** send a new request so its diff uses the latest source.

API contract checked against [Cloud](https://docs.ollama.com/cloud),
[authentication](https://docs.ollama.com/api/authentication) and
[chat](https://docs.ollama.com/api/chat) documentation on 2026-10-27.
Automated tests use an in-process HTTP transport and do not call a paid model. No live
inference was verified during development because no Ollama API key was configured.
