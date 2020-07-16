from raiden.network.proxies.token_network import ChannelDetails, TokenNetwork
from raiden.transfer.state import Claim, NettingChannelState, PendingLocksState
from raiden.utils.typing import (
    AdditionalHash,
    Address,
    BalanceHash,
    BlockExpiration,
    BlockIdentifier,
    BlockTimeout,
    LockedAmount,
    Locksroot,
    Nonce,
    Signature,
    TokenAddress,
    TokenAmount,
    WithdrawAmount,
)
from raiden_contracts.contract_manager import ContractManager


class PaymentChannel:
    def __init__(
        self,
        token_network: TokenNetwork,
        channel_state: NettingChannelState,
        contract_manager: ContractManager,
    ):
        self.channel_identifier = channel_state.canonical_identifier.channel_identifier
        self.participant1 = channel_state.our_state.address
        self.participant2 = channel_state.partner_state.address
        self.token_network = token_network
        self.client = token_network.client
        self.contract_manager = contract_manager

    def token_address(self) -> TokenAddress:
        """ Returns the address of the token for the channel. """
        return self.token_network.token_address()

    def detail(self, block_identifier: BlockIdentifier) -> ChannelDetails:
        """ Returns the channel details. """
        return self.token_network.detail(
            participant1=self.participant1,
            participant2=self.participant2,
            block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
        )

    def settle_timeout(self) -> BlockTimeout:
        """ Returns the channels settle_timeout. """
        return BlockTimeout(self.token_network.settlement_timeout_min())

    def opened(self, block_identifier: BlockIdentifier) -> bool:
        """ Returns if the channel is opened. """
        return self.token_network.channel_is_opened(
            participant1=self.participant1,
            participant2=self.participant2,
            block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
        )

    def closed(self, block_identifier: BlockIdentifier) -> bool:
        """ Returns if the channel is closed. """
        return self.token_network.channel_is_closed(
            participant1=self.participant1,
            participant2=self.participant2,
            block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
        )

    def settled(self, block_identifier: BlockIdentifier) -> bool:
        """ Returns if the channel is settled. """
        return self.token_network.channel_is_settled(
            participant1=self.participant1,
            participant2=self.participant2,
            block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
        )

    def can_transfer(self, block_identifier: BlockIdentifier) -> bool:
        """ Returns True if the channel is opened and the node has deposit in it. """
        return self.token_network.can_transfer(
            participant1=self.participant1,
            participant2=self.participant2,
            block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
        )

    def approve_and_set_total_deposit(
        self, total_deposit: TokenAmount, block_identifier: BlockIdentifier
    ) -> None:
        self.token_network.approve_and_set_total_deposit(
            given_block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
            total_deposit=total_deposit,
            partner=self.participant2,
        )

    def set_total_withdraw(
        self,
        total_withdraw: WithdrawAmount,
        participant_signature: Signature,
        partner_signature: Signature,
        expiration_block: BlockExpiration,
        block_identifier: BlockIdentifier,
    ) -> None:
        self.token_network.set_total_withdraw(
            given_block_identifier=block_identifier,
            channel_identifier=self.channel_identifier,
            total_withdraw=total_withdraw,
            expiration_block=expiration_block,
            participant_signature=participant_signature,
            partner_signature=partner_signature,
            participant=self.participant1,
            partner=self.participant2,
        )

    def close(
        self,
        nonce: Nonce,
        balance_hash: BalanceHash,
        additional_hash: AdditionalHash,
        non_closing_signature: Signature,
        closing_signature: Signature,
        block_identifier: BlockIdentifier,
    ) -> None:
        """ Closes the channel using the provided balance proof, and our closing signature. """
        self.token_network.close(
            channel_identifier=self.channel_identifier,
            partner=self.participant2,
            balance_hash=balance_hash,
            nonce=nonce,
            additional_hash=additional_hash,
            non_closing_signature=non_closing_signature,
            closing_signature=closing_signature,
            given_block_identifier=block_identifier,
        )

    def update_transfer(
        self,
        nonce: Nonce,
        balance_hash: BalanceHash,
        additional_hash: AdditionalHash,
        partner_signature: Signature,
        signature: Signature,
        block_identifier: BlockIdentifier,
    ) -> None:
        """ Updates the channel using the provided balance proof. """
        self.token_network.update_transfer(
            channel_identifier=self.channel_identifier,
            partner=self.participant2,
            balance_hash=balance_hash,
            nonce=nonce,
            additional_hash=additional_hash,
            closing_signature=partner_signature,
            non_closing_signature=signature,
            given_block_identifier=block_identifier,
        )

    def unlock(
        self,
        sender: Address,
        receiver: Address,
        pending_locks: PendingLocksState,
        given_block_identifier: BlockIdentifier,
    ) -> None:
        self.token_network.unlock(
            channel_identifier=self.channel_identifier,
            sender=sender,
            receiver=receiver,
            pending_locks=pending_locks,
            given_block_identifier=given_block_identifier,
        )

    def settle(
        self,
        transferred_amount: TokenAmount,
        locked_amount: LockedAmount,
        locksroot: Locksroot,
        claim: Claim,
        partner_transferred_amount: TokenAmount,
        partner_locked_amount: LockedAmount,
        partner_locksroot: Locksroot,
        partner_claim: Claim,
        block_identifier: BlockIdentifier,
    ) -> None:
        """ Settles the channel. """
        self.token_network.settle(
            channel_identifier=self.channel_identifier,
            transferred_amount=transferred_amount,
            locked_amount=locked_amount,
            locksroot=locksroot,
            claim=claim,
            partner=self.participant2,
            partner_transferred_amount=partner_transferred_amount,
            partner_locked_amount=partner_locked_amount,
            partner_locksroot=partner_locksroot,
            partner_claim=partner_claim,
            given_block_identifier=block_identifier,
        )
