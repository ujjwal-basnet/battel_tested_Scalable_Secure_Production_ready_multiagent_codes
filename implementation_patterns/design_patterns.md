
1) Adapter Pattern For Legacy Sytem
When integrating
with a legacy system that doesn't have a modern REST API, build
a dedicated "Adapter" service. This service acts as a translator,
exposing a clean, modern API to the LangChain application and
handling the complexity of interacting with the legacy system
(e.g., via SOAP, file drops, or direct database connections).

### what we are building on this section 
###     we are building question answering that first attempts to answer a question using a hight quality but expensive model. If that model fails for any reason (api outrage , rage limits )