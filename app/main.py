from app.infrastructure.api.fastapi import app, Depends

from app.api import check
from app.api import cliente
from app.api import pagamento
from app.api import pedido
from app.api import produto
from app.api import status_pedido
from app.webhooks import pagamento as pagamento_webhook

# declare
app.include_router(check.router)
app.include_router(cliente.router)
app.include_router(pagamento.router)
app.include_router(pedido.router)
app.include_router(produto.router)
app.include_router(status_pedido.router)
app.include_router(pagamento_webhook.router)